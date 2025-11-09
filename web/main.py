from flask import Flask, render_template, request, flash, redirect, url_for
from our_data import *


app = Flask(__name__)
app.secret_key = 'your_very_secret_key_change_me_123456'
@app.route('/')
def hellow():
    return render_template('welcome.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signupForm', methods=['POST'])
def login_to_system():
    print(request.form)
    name = request.form.get('Name')
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    confirm_password = request.form.get('confirmPassword')
    # Validate that passwords match
    if password != confirm_password:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('signup'))
    try:
        user().insert(name, email, password, username)
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    except:
        flash('username already used, please try another one', 'error')
        return redirect(url_for('signup'))



if __name__ == '__main__':
    app.run(debug=True)