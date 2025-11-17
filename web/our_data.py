import hashlib
import sqlite3
from calendar import error

import bcrypt

def start():
    conn = None
    try:
        conn = sqlite3.connect('our_data.db')
        return conn
    except:
        print("there was an error")
    return conn

def close_conn(conn):
    conn.close()

class user:

    def __init__(self):
        self.conn = start()

    def hash_fun(self, ptext):
        ptext_bytes = ptext.encode('utf-8')
        hasher = hashlib.sha256()
        hasher.update(ptext_bytes)
        return hasher.hexdigest()

    def insert(self,username, password,email,name):
        users = self.display_all_records()
        for user in users:
            if username == user[1]:
                raise error
        password = self.hash_fun(password)
        sql = "INSERT INTO user(username,password,email,name) VALUES(?,?,?,?)"
        cursor = self.conn.cursor()
        cursor.execute(sql,(username, password,email,name))
        self.conn.commit()


    def display_all_records(self):
        try:
            sql = 'select * from user'
            cur = self.conn.cursor()
            cur.execute(sql)
            x = cur.fetchall()
            return x
        except: return ""

    def display_record(self,uid):
        try:
            sql = 'select * from user where uid=?'
            cur = self.conn.cursor()
            cur.execute(sql, (uid,))
            x = cur.fetchone()
            return x
        except: return ""

    def login(self, username, password):
        users = self.display_all_records()
        x = []
        for user in users:
            if username == user[1]:
                x = user
                break
        if x == []:
            return 0
        password = self.hash_fun(password)
        print(password)
        print(x)
        if str(password) == str(x[2]):
            return x

        return 1

    def get_user(self, username):
        sql = 'select * from user where username=?'
        cursor = self.conn.cursor()
        cursor.execute(sql, (username,))
        x = cursor.fetchone()
        return x


class money:

    def __init__(self,uid):
        self.uid = uid
        self.conn = start()

    def insert(self,name,amount, exp_or_inc , date, description):
        if exp_or_inc == 0:
            if (int(amount) + int(self.total_expenses())) > self.total_income():
                raise error
        sql = "INSERT INTO trans (uid,name,amount, exp_or_inc, time, desc) VALUES(?,?,?,?,?,?)"
        cursor = self.conn.cursor()
        cursor.execute(sql, (self.uid,name,amount,exp_or_inc,date,description))
        self.conn.commit()

    def total_income(self):
        sql = "SELECT SUM(amount) FROM trans where uid=? and exp_or_inc = 1"
        cursor = self.conn.cursor()
        cursor.execute(sql, (self.uid,))
        x = cursor.fetchone()
        return x[0]

    def total_expenses(self):
        sql = "SELECT SUM(amount) FROM trans where uid=? and exp_or_inc = 0"
        cursor = self.conn.cursor()
        cursor.execute(sql, (self.uid,))
        x = cursor.fetchone()[0]
        if x == None:
            return 0
        return x

    def balance(self):
        b = self.total_income() - self.total_expenses()
        return b

    # def update_income(self,id,name,amount):
    #     sql = "update income set name=?,amount=? where eid=?"
    #     cursor = self.conn.cursor()
    #     cursor.execute(sql, (name,amount,id))
    #     self.conn.commit()
    #
    # def update_expenses(self,id,name,amount):
    #     sql = "update expenses set name=?,amount=? where eid=?"
    #     cursor = self.conn.cursor()
    #     cursor.execute(sql, (name,amount,id))
    #     self.conn.commit()
    #
    # def delete_income(self,eid):
    #     sql = "delete from income where eid=?"
    #     cursor = self.conn.cursor()
    #     cursor.execute(sql, (eid,))
    #     self.conn.commit()
    #
    # def delete_expenses(self,eid):
    #     sql = "delete from expenses where eid=?"
    #     cursor = self.conn.cursor()
    #     cursor.execute(sql, (eid,))
    #     self.conn.commit()

    # def display_income(self,eid):
    #     sql = "select * from expenses where eid=?"
    #     cursor = self.conn.cursor()
    #     cursor.execute(sql, (eid,))
    #     return cursor.fetchone()

    def display_all_expenses(self):
        sql = "select * from trans where uid=? and exp_or_inc = 0"
        cursor = self.conn.cursor()
        cursor.execute(sql, (self.uid,))
        return cursor.fetchall()

    def display_all_income(self):
        sql = "select * from trans where uid=? and exp_or_inc = 1 "
        cursor = self.conn.cursor()
        cursor.execute(sql, (self.uid,))
        return cursor.fetchall()


if __name__ == '__main__':
    user = user()
    #user.insert('2','2','2','2')
    print(user.login('4','4'))
    money = money(10)
    money.add('salary',990)
    print(money.sub('grocery',200))
    print(money.balance())
    print(money.total_income())
    print(money.total_expenses())
    print(money.display_all_expenses())
    print(money.display_all_income())


