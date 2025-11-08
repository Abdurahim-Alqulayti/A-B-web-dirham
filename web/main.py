from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def hellow():
    return render_template('welcome.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)