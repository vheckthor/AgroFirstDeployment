import os
import requests # to use this library please download and install the requests library
import urllib.parse
from flask import redirect, render_template, request, session
from functools import wraps
import sqlite3 as sql
from os import path
ROOT = path.dirname(path.relpath((__file__)))

#this function helps to communicate with the database
def create_post(firstname, lastname,email,phonenumber,password,checkbox,image ):
    #this call the database
    con = sql.connect(path.join(ROOT, "database.db"))
    #this hewlp to traverse through our database efficiently
    cur = con.cursor()
    if  checkbox=="": 
        cur.execute('insert into users(firstname,lastname,email,phonenumber,password,image) values(?, ?,?,?,?,?)',(firstname,lastname,email,phonenumber,password,image))
        con.commit()
        con.close()
    else:   
        cur.execute('insert into farmers(firstname,lastname,email,password,phonenumber,checkbox,image) values(?,?, ?,?,?,?,?)',(firstname,lastname,email,password,phonenumber,checkbox,image))
        con.commit()
        con.close()

###########create post method for investment
def create_invest(firstname,lastname,phonenumber,phonenumber2,category,location,fundneeded,image,interest,description,title,farmerid,date):
    #this call the database
    con = sql.connect(path.join(ROOT, "database.db"))
    #this hewlp to traverse through our database efficiently
    cur = con.cursor() 
    cur.execute('insert into investment(firstname,lastname,phonenumber,phonenumber2,category,location,fundneeded,image,interest,description,title,farmerid,date) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',(firstname,lastname,phonenumber,phonenumber2,category,location,fundneeded,image,interest,description,title,farmerid,date))
    con.commit()
    con.close()
##############create for sales
def create_sell(firstname,lastname,phonenumber,phonenumber2,location,quantity,price,product,description,farmerid,date,image,category):
    #this call the database
    con = sql.connect(path.join(ROOT, "database.db"))
    #this hewlp to traverse through our database efficiently
    cur = con.cursor() 
    cur.execute('insert into sell(firstname,lastname,phonenumber,phonenumber2,location,quantity,price,product,description,farmerid,date,image,category) values(?, ?,?,?,?,?,?,?,?,?,?,?,?)',(firstname,lastname,phonenumber,phonenumber2,location,quantity,price,product,description,farmerid,date,image,category))
    con.commit()
    con.close()


###################create investor
def create_investor(firstname,lastname,email,invested,userid):
    #this call the database
    con = sql.connect(path.join(ROOT, "database.db"))
    #this hewlp to traverse through our database efficiently
    cur = con.cursor() 
    cur.execute('insert into investor(firstname,lastname,email,invested,userid) values(?, ?,?,?,?,?)',(firstname,lastname,email,invested,userid))
    con.commit()
    con.close()


#################update
########update invest
def update_invest(firstname,lastname,phonenumber,phonenumber2,category,location,fundneeded,image,interest,description,title,farmerid,date,val):
    #this call the database
    con = sql.connect(path.join(ROOT, "database.db"))
    #this help to traverse through our database efficiently
    cur = con.cursor()
    sqlquery= """Update investment set firstname= ?, lastname= ?, phonenumber= ?, phonenumber2= ?,category= ?,location= ?,fundneeded= ?,image= ?,interest= ?,\
        description= ?,title= ?,farmerid= ?,date= ? WHERE id=?"""# = ?,?,?,?,?,?,?,?,?,?,?,?,?" 
    # letwhere=  (f"WHERE {ld}=?",(nd))
    dothing = (firstname,lastname,phonenumber,phonenumber2,category,location,fundneeded,image,interest,description,title,farmerid,date,val)
    cur.execute(sqlquery,dothing)
    con.commit()
    con.close()
########update sell
def update_sell(firstname,lastname,phonenumber,phonenumber2,location,quantity,price,product,description,farmerid,date,image,category,our):
    #this call the database
    con = sql.connect(path.join(ROOT, "database.db"))
    #this help to traverse through our database efficiently
    cur = con.cursor()
    sqlquery= """Update sell set firstname=?,lastname=?,phonenumber=?,phonenumber2=?,location=?,quantity=?,price=?,\
        product=?,description=?,farmerid=?,date=?,image=?,category=? WHERE id  = ?"""# = ?,?,?,?,?,?,?,?,?,?,?,?,?" 
    dothing = (firstname,lastname,phonenumber,phonenumber2,location,quantity,price,product,description,farmerid,date,image,category,our)
    cur.execute(sqlquery,dothing)
    con.commit()
    con.close()
    

######get methodes for communication with the DB
def get_posts(who,what,why,whit):
    con = sql.connect(path.join(ROOT, "database.db"))
    cur = con.cursor()
    cur.execute(f"SELECT {who} FROM {what} WHERE {why} = ? ",(whit,))
    posts = cur.fetchall()
    return posts

def get_investment(who,what,why,whit):
    con = sql.connect(path.join(ROOT, "database.db"))
    cur = con.cursor()
    cur.execute(f"SELECT {who} FROM {what} WHERE {why} = ? ",(whit,))
    posts = cur.fetchall()
    return posts

#####################this is to get investment
def get_sell(who,what,why,whit):
    con = sql.connect(path.join(ROOT, "database.db"))
    cur = con.cursor()
    cur.execute(f"SELECT {who} FROM {what} WHERE {why} = ? ",(whit,))
    posts = cur.fetchall()
    return posts
########getsell 2
def get_sell2(who,what):
    con = sql.connect(path.join(ROOT, "database.db"))
    cur = con.cursor()
    cur.execute(f"SELECT {who} FROM {what}")
    posts = cur.fetchall()
    return posts


#####route to delete from db
def delete_task(place,id):
  #  """
    # Delete a task by task id
    # :param conn:  Connection to the SQLite database
    # :param id: id of the task
    # :return:
    # """
    conn = sql.connect(path.join(ROOT, "database.db"))
    cur = conn.cursor()
    cur.execute(f'DELETE FROM {place} WHERE id=?', (id,))
    conn.commit()

######apology page
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code
    
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
