import os
from flask import Flask, request, session, redirect, url_for, escape

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s. <a href="/logout">Logout</a>' % escape(session['username'])
    return 'You are not logged in. <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('index'))
    return '''
    <form action="/login" method="POST">
        <p>Username <input type="text" name="username" /></p>
        <p><input type="submit" value="Login" /></p>
    </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)