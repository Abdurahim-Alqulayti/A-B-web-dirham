import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import our_data
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('UI2.html')
@app.route('/load_data_form', methods=['POST'])
def calc_sum():
    try:
        x = our_data.expen(2)
        a = x.display_all()
        total = x.total_expenses()
        remaining =our_data.user().display_record(2)[4] - total

        return render_template('UI2.html',value=a,total=total,remaining=remaining)
    except:
        return render_template('UI2.html', result="Error")


if __name__ == '__main__':
    app.run(host='localhost',port='5555', debug=True)
