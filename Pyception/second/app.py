from flask import Flask, render_template, request, url_for, redirect
import io,sys
app = Flask(__name__)

def test(code):
  if code[0] == '"' and code[-1] == '"' and all(ch != '"' for ch in code[1:-1]):
    output_stream = io.StringIO()
    compiled = compile('code = print("' + eval(code) + '")', "out", mode = "exec")

    sys.stdout = output_stream
    exec(compiled, globals())
    sys.stdout = sys.__stdout__

    return output_stream.getvalue()

  else:
    return ":< Told you I need input in double quote and double quote inside double quote is not allowed"

@app.route('/', methods=['GET','POST'])
def HomePage():
    te = '"Output will be displayed here!!"'
    if request.method == 'POST':
      te = request.form['text']
      return render_template('index.html',output=test(te))
    else:
       return render_template('index.html')

@app.route('/static/flag.txt')
def not_allowed():
    return redirect('/')

@app.route('/app.py')
def not_allowed2():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False)