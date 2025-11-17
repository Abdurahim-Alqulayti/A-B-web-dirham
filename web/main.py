from flask import Flask, render_template, request, flash, redirect, url_for
from our_data import user as USER, money


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
        USER().insert(username, password, email, name)
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    except:
        flash('username already used, please try another one', 'error')
        return redirect(url_for('signup'))

@app.route('/loginForm', methods=['POST'])
def login_form():
    username = request.form.get('username')
    password = request.form.get('password')
    val = USER().login(username, password)
    if val == 0 or val == 1:
        flash('Login failed.', 'error')
        return redirect(url_for('login'))
    user = USER().get_user(username)[0]
    inc, exp, balance,general_table,name ,inc_tup,exp_tup = user_info(user)
    print(user)
    return render_template('UI2.html',
                           income=inc, expense=exp,
                           balance=balance, general=general_table,
                           name=name, income_breakdown=inc_tup,
                           expense_breakdown=exp_tup , user = user)


def user_info(user_id):
    id = user_id
    name = USER().display_record(id)[-1]
    wallet = money(id)
    inc = wallet.total_income()
    exp = wallet.total_expenses()
    exp_table = wallet.display_all_expenses()
    inc_table = wallet.display_all_income()
    exp_tup = []
    exp_dic = {}
    for i in exp_table:
        exp_dic[i[2]] = exp_dic.get(i[2], 0) + i[3]
    for k, v in exp_dic.items():
        perc = v / exp if exp else 0
        exp_tup.append((k, perc * 100, v))
    inc_dic = {}
    inc_tup = []
    for i in inc_table:
        inc_dic[i[2]] = inc_dic.get(i[2], 0) + i[3]
    for k, v in inc_dic.items():
        perc = v / inc if inc else 0
        inc_tup.append((k, perc * 100, v))
    general_table = exp_table + inc_table
    print(general_table)
    general_table = sorted(general_table, key=lambda x: x[-3], reverse=True)
    return inc, exp, wallet.balance(), general_table,name, inc_tup, exp_tup

@app.route('/UI2/<user>')
def UI2(user):
    print(user)
    inc, exp, balance,general_table,name ,inc_tup,exp_tup  = user_info(user)
    return render_template('UI2.html',
                           income=inc, expense=exp,
                           balance=balance, general=general_table,
                           name=name, income_breakdown=inc_tup,
                           expense_breakdown=exp_tup, user = user)

@app.route('/transaction/<user>')
def transaction(user):
    print(user)
    return render_template('transaction.html', user=user)

@app.route('/add_transaction/<user>', methods=['POST'])
def add_transaction(user):
    amount = request.form.get('amount')
    inc_or_exp = int(request.form.get('transaction_type'))
    type = request.form.get('category')
    date = request.form.get('date')
    description = request.form.get('description')
    wallet = money(user)
    wallet.insert(type,amount, inc_or_exp, date, description)
    return render_template('transaction.html',user =user)


if __name__ == '__main__':
    app.run(debug=True)