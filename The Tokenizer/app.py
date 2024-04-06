from flask import Flask, jsonify, make_response, request,render_template,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime
import hashlib

app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

pub_key = open('public_key.pem','rb').read()
pri_key = open('private_key.pem','rb').read()

app.secret = "0CTF{S3ns4tional_Sw33t_Tr3ats_with_JWT_Surpris3s}"

db = SQLAlchemy(app)

class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   public_id = db.Column(db.Integer)
   name = db.Column(db.String(50))
   password = db.Column(db.String(50))
   admin = db.Column(db.Boolean)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if request.cookies:
            token = request.cookies.get('token')
            if token:
                try:
                    data = jwt.decode(token, pub_key, algorithms=["RS256"])
                    isadmin = data.get('admin')
                    current_user = Users.query.filter_by(public_id=data['public_id']).first()

                    return f(current_user, isadmin, *args, **kwargs)
                except Exception as e:
                    return jsonify({'message': 'Invalid token'+str(e)})
            else:
                return jsonify({'message': 'Token not found'})
            
        return f(current_user,isadmin,*args, **kwargs)
    return decorator

@app.route('/',methods=['GET'])
def change_location():
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def signup_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password: 
            return make_response('could not verify', 401, {'Authentication': 'login required"'})

        existing_user = Users.query.filter_by(name=username).first()

        if existing_user:
            return jsonify({'message': 'User already exists!'})

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = Users(public_id=str(uuid.uuid4()), name=username, password=hashed_password, admin=False)
        db.session.add(new_user) 
        db.session.commit()

        return jsonify({'message': 'registered successfully'})
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET','POST']) 
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password: 
            return make_response('could not verify', 401, {'Authentication': 'login required"'})   

        user = Users.query.filter_by(name=username).first()
        if user:
            if user and check_password_hash(user.password, password):
                token = jwt.encode({'user':username,'public_id' : user.public_id,'admin':user.admin, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1365)}, pri_key, "RS256")
                response = make_response(redirect('/welcome'))
                response.set_cookie('token', token, secure=True, httponly=True, samesite='Strict')
                return response
            else:
                return make_response('Invalid username or password', 401, {'Authentication': 'Invalid username or password'})
        else:
            return make_response('Invalid username or password', 401, {'Authentication': 'Invalid username or password'})
    else:
        return render_template('login.html')

@app.route('/welcome',methods=['GET'])
@token_required
def welcome(current_user,isadmin):
    return render_template('welcome.html')

@app.route('/admin', methods=['GET'])
@token_required
def admin_route(current_user,isadmin):
    if isadmin:
        return jsonify({'message': 'Welcome Admin!','flag':app.secret})
    else:
        return jsonify({'message': 'this page is for admin only'})

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@token_required
def key_collection(current_user, isadmin):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            file_data = file.read()
            uploaded_hash = hashlib.md5(file_data).hexdigest()
            saved_hash = "253dd04e87492e4fc3471de5e776bc3d"

            if uploaded_hash == saved_hash:
                result = "Image authenticated successfully!"
                pri_key_str = pri_key.decode('utf-8')
                return jsonify({'message': result, 'Private key': pri_key_str}), 200
            else:
                result = "Image authentication failed!"
                return jsonify({'message': result}), 401
        else:
            return jsonify({'message': 'Invalid file type. Only JPG, JPEG, and PNG files are allowed.'}), 400
    else:
        return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=False,port=9999)