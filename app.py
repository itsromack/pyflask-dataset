import os, dataset, MySQLdb
from flask import Flask, request, session, redirect, url_for, escape
from hashlib import sha256

app = Flask(__name__)
app.secret_key = os.urandom(24)

db = dataset.connect('mysql://root:secret123@localhost/test')
users = db['users']

@app.route('/')
def index():
    if 'user_id' in session:
        return 'Logged in as %s. <a href="/logout">Logout</a>' % escape(session['username'])
    return 'You are not logged in. <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_exists(username, password):
            return redirect(url_for('index'))
    return '''
    <form action="/login" method="POST">
        <p>Username <input type="text" name="username" /></p>
        <p>Password <input type="password" name="password" /></p>
        <p><input type="submit" value="Login" /></p>
    </form>
    '''

def user_exists(username, password):
    hashed_password = sha256(password.encode())
    row = users.find_one(username=username, pass_word=hashed_password.hexdigest())
    if row == None:
        return False
    session['user_id'] = row['id']
    session['username'] = row['username']
    return True


@app.route('/logout')
def logout():
    session.pop('user_id')
    session.pop('username')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)