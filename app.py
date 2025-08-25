from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ---------- HOME PAGE = LOGIN ----------
@app.route('/')
def home():
    return render_template('login.html')   # loads templates/login.html

# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    try:
        with open('data.txt', 'r') as file:
            users = file.readlines()
    except FileNotFoundError:
        users = []

    for user in users:
        saved_username, saved_password = user.strip().split('|')
        if saved_username == username and saved_password == password:
            return redirect(url_for('dashboard', username=username))

    return "❌ Invalid username or password! <a href='/'>Try again</a>"

# ---------- SIGNUP ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "⚠️ Passwords do not match! <a href='/signup'>Try again</a>"

        with open('data.txt', 'a') as file:
            file.write(f"{username}|{password}\n")

        return redirect('/')

    return render_template('signup.html')

# ---------- DASHBOARD ----------
@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template('dashboard.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
