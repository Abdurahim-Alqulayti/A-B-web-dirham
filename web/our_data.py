import sqlite3
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
        px = ptext
        px = px.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(px, salt)
        return hash

    def insert(self, mame, email, password, username):
        password = self.hash_fun(password)
        sql = "INSERT INTO user(name,email,password, username) VALUES(?,?,?,?)"
        cursor = self.conn.cursor()
        cursor.execute(sql,(mame,email,password,username))
        self.conn.commit()
        close_conn(self.conn)


    # def insert_record(self, username,password):
    #     user = (username,self.hash_fun(password))
    #     if not self.auth_user((username,password)):
    #         sql = 'INSERT INTO users(username,password,type,pic,money) VALUES(?,?,?,?,?)'
    #         cur = self.conn.cursor()
    #         cur.execute(sql, (user[0], user[1], type,"p_pic/empty-profile.png",0))
    #         self.conn.commit()
    #     else:
    #         return "User already exist"

    # def delete_record(self, id):
    #     sql = 'DELETE from users where id = ?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql, (id,))
    #     self.conn.commit()
    #
    # def delete_all_record(self):
    #     sql = 'DELETE from users'
    #     cur = self.conn.cursor()
    #     cur.execute(sql)
    #     self.conn.commit()
    #
    # def update_record(self, id,username,password,type):
    #     sql = 'UPDATE users SET username=?,password=?,type=? where id=?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql, (username,password.hash(),type, id))
    #     self.conn.commit()
    #
    # def reset_password(self, id, password):
    #     sql = 'UPDATE users SET password=? where id=?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql, (self.hash_fun(password), id))
    #     self.conn.commit()
    #
    # def reset_name(self, id, name):
    #     sql = 'UPDATE users SET username=? where id=?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql, (name, id))
    #     self.conn.commit()
    #
    # def reset_pic(self, id, pic):
    #     sql = 'UPDATE users SET pic=? where id=?'
    #     print(pic)
    #     cur = self.conn.cursor()
    #     cur.execute(sql, (pic, id))
    #     self.conn.commit()
    # def get_name(self, id):
    #     sql = 'SELECT username FROM users WHERE id = ?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql, (id,))
    #     return cur.fetchone()[0]
    #
    # def get_pic(self,id):
    #     sql = 'select pic from users where id = ?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql,(id,))
    #     x = cur.fetchone()[0]
    #     print(x)
    #     return x

    def auth_user(self, user):
        sql = 'SELECT * FROM users where username = ? '
        cur = self.conn.cursor()
        cur.execute(sql, (user[0],))
        x = cur.fetchall()
        for i in x:
            if bcrypt.checkpw(user[1].encode("utf-8"), i[2]):
                return True
        return False

    # def get_type(self,user):
    #     sql = 'SELECT * FROM users where username = ? '
    #     cur = self.conn.cursor()
    #     cur.execute(sql, (user[0],))
    #     x = cur.fetchall()
    #     y = []
    #     for i in x:
    #         if bcrypt.checkpw(user[1].encode("utf-8"), i[2]):
    #             return i[3]
    #     return False
    #
    # def get_id(self,user):
    #     sql = 'SELECT * FROM users where username = ? '
    #     cur = self.conn.cursor()
    #     cur.execute(sql, (user[0],))
    #     x = cur.fetchall()
    #     return x[0]
    #
    #
    #
    # def display_all_records(self):
    #     sql = 'select * from users'
    #     cur = self.conn.cursor()
    #     cur.execute(sql)
    #     x = cur.fetchall()
    #     return x
    #
    #
    # def display_record(self, id):
    #     sql = 'select * from users where id=?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql, (id,))
    #     row = cur.fetchone()
    #     return row
    #
    # def add_money_to_user(self,user,money):
    #     sql = 'UPDATE users SET money =  ? WHERE id = ?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql,(money ,user))
    #     self.conn.commit()
    #
    #
    #
    # def get_palace(self,id):
    #     sql = 'select money from users where id = ?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql,(id,))
    #     x = cur.fetchone()[0]
    #     return x
    #
    # def set_palace(self,id,money):
    #     sql = 'UPDATE users SET money = money + ? WHERE id = ?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql,(money,id))
    #     self.conn.commit()
    #
    # def decrease_money(self,id,money):
    #     sql = 'UPDATE users SET money = money - ? WHERE id = ?'
    #     cur = self.conn.cursor()
    #     cur.execute(sql,(money,id))
    #     self.conn.commit()
    #
    # def increase_money(self, products, cart):
    #     for product in products:
    #         sid = product[-1]
    #         total = cart[product] * product[4]
    #         prof = total * 0.01
    #         total = total - prof
    #         sql = 'UPDATE users SET money = money + ? WHERE id = ?'
    #         cur = self.conn.cursor()
    #         cur.execute(sql,(total,sid))
    #         self.conn.commit()
    #         sql = 'UPDATE users SET money = money + ? WHERE id = ?'
    #         cur = self.conn.cursor()
    #         cur.execute(sql, (prof, 20))
    #         self.conn.commit()