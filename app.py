from flask import Flask,render_template,g,request,flash,redirect,url_for,session,flash
from functools import wraps
import sqlite3
import os
app = Flask(__name__)
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

app.secret_key = os.urandom(24)
app.database='sample.db'
conn=sqlite3.connect('sample.db')


@app.route('/welcome')
def welcome():
 return render_template('welcome.html')


@app.route('/home')
@login_required
def home():
 return render_template('home.html')

@app.route('/sef')
def sef():
 return render_template('search.html')

@app.route('/sef1')
def sef1():
 return render_template('search1.html')

@app.route('/del')
def delt():
 return render_template('del.html')

@app.route('/stud', methods=['GET','POST'])
def stud():
 return render_template('stud.html')

@app.route('/', methods=['GET','POST'])
def login():
   error = None
   if request.method == 'POST':
    if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
    else:
            session['logged_in']=True 
            return redirect(url_for('welcome'))
	    flash('!You were just logged in!!')
   return render_template('login.html', error=error)


@app.route('/rec')
def rec(): 
 g.db = connect_db() 
 cur = g.db.execute('select name,mark1,mark2,total,grade from students')
 
 row = cur.fetchall()  
 return render_template('index.html',row=row)
@app.route('/rec1')
def rec1(): 
 g.db = connect_db() 
 cur = g.db.execute('select name,mark1,mark2,total,grade from students')
 
 row = cur.fetchall()  
 return render_template('index1.html',row=row)
@app.route('/ser',methods=['POST'])
def ser():
 
 g.db = connect_db()
 cur=g.db.execute( "select * from students where name = ? ", (request.form['search'],) )
 row = cur.fetchall()
 return render_template("index.html",row=row)


@app.route('/ser1',methods=['POST'])
def ser1():
 
 g.db = connect_db()
 cur=g.db.execute( "select * from students where name = ? ", (request.form['search'],) )
 row = cur.fetchall()
 return render_template("index1.html",row=row)


@app.route('/logout')
@login_required
def logout():
 session.pop('logged_in',None)
 flash('!!You were just logged out')
 return redirect(url_for('login'))

@app.route('/delete',methods=['POST'])
def delete():
 g.db = connect_db()
 g.db.execute( "delete from students where name = ? ", (request.form['delete'],) )
 g.db.commit()
 cur=g.db.execute( "select * from students ")
 row=cur.fetchall()
 return render_template("delete.html",row=row) 


@app.route('/add', methods=['POST'])
def add():
 g.db=connect_db()
             
 g.db.execute('INSERT INTO students (name,mark1,mark2,total,grade) VALUES(?,?,?,?,?)',[request.form['name'],request.form['mark1'],request.form['mark2'],request.form['total'],request.form['grade']]);
 g.db.commit()
 flash('posted')
 return redirect(url_for('home'))


@app.route('/search')
def search():
 return render_template("search.html")
def connect_db():
 return sqlite3.connect(app.database)




if __name__ == '__main__':
 app.run(debug=True)
