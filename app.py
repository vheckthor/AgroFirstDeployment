import os
import cs50
from flask import Flask, render_template, request,flash,request,session,redirect
import requests
from flask_session import Session
from tempfile import mkdtemp
import datetime
import random
from flask_cors import CORS
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import models
from models import get_sell2,create_post, get_posts,apology,login_required,get_investment, create_invest,create_sell,get_sell,  delete_task,update_invest,update_sell,create_investor
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
#to auto reload pages
app.config["TEMPLATES_AUTO_RELOAD"] = True

 #to upload pictures in our program
photos =UploadSet("photos",IMAGES)

app.config["UPLOADED_PHOTOS_DEST"] = 'static/images/gallery'
configure_uploads(app, photos)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['GET'])
def index():
    if  request.method=='GET':
        row3 = get_sell2("*", "sell")
        #print(row3)
        if len(row3) >= 6:
           # for i in range(6):
            # x =  random.randint(1,len(row3))
            # y = random.randint((len(row3)-1),len(row3))
            row = row3[0:6]
            print(row)
            return render_template("index.html",row=row)
        else:
   # return render_template("history.html",row3=row3)
            return render_template("index.html")

####this route return the registeration page for those who failed to create account before login
@app.route('/register',methods=['GET'])
def register():
    return render_template("register.html")
 #####About route fixed
 ##########investor page
@app.route('/investor',methods=['GET','POST'])
def investorform():
    ses = session.get("user_id")
    emailid =session.get("email")
    if not ses:
        return render_template("investlogin.html")
    return render_template("investorform.html")

@app.route('/investorpop',methods=['POST'])
def investorpop():
    ses = session.get("user_id")
    emailid =session.get("email")
    if request. method=='POST':
        print ("I am here")
        data = request.get_json()
        print(data)
        new_freq = data
        print (new_freq)
        userid = ses
        invested = new_freq
        farmers = get_posts("*", "farmers", "id", ses)
        print(farmers)
        users = get_posts("*", "users", "id", ses)
        print(users)
        print("farmers are great")
        if len(farmers)==1 and farmers[0][3] == emailid:
            firstname =farmers[0][1]
            lastname =farmers[0][2]
            email = farmers[0][3]
            create_investor(firstname,lastname,email,invested,userid)
        elif len(users)==1 and users[0][3]==emailid: 
            firstname =users[0][1]
            lastname =users[0][2]
            email = users[0][3]
        create_investor(firstname,lastname,email,invested,userid)

    ######about route
@app.route('/about',methods=['GET'])
def about():
    return render_template("about.html")
#####this route help delete a specific element buy it id
@app.route('/del',methods=['POST'])
def delete():
    if request.method=='POST':
        print("we thank thee")
        ld = request.form.get("de")
        print(ld)       
        delete_task("sell",ld)
    return redirect("/farmers")

####delete investment
@app.route('/deli',methods=['POST'])
def deleteinvest():
    if request.method=='POST':
        print("we thank thee")
        ld = request.form.get("de")
        print(ld)
        delete_task("investment",ld)
    return redirect("/farmers")
##########################this is to update into database for seller
@app.route('/updatese',methods=['POST'])
def updatese():
    if request.method =='POST':
        print("i am here")
        idp = request.form.get("de")
        sell = get_sell("*","sell","id",idp)
        session["bug"]=idp
        return render_template("updatesell.html",sell=sell)

@app.route("/updatesell",methods=["POST"])
#@login_required
def updatesell():
    """Show farmers details"""
    sessionid = session.get("user_id")
    our =session["bug"]
    print(sessionid)
    if request.method=="POST" and 'photo' in request.files:
        if not request.form.get("firstname"):
            return  apology(" Go back and  enter your first name",400)
        if not request.form.get("category"):
            return apology("Go back and  specify the category of farm you run",400)
        if not request.form.get("lastname"):
            return apology(" Please go back and enter your last name ",400)
        if not request.form.get("phonenumber"):
            return apology("Go back and  enter your phone number",400)
        if not request.form.get("location"):
            return apology("Error  Go back and  enter the location of your farm",400)
        if not request.form.get("product"):
            return apology("Error  Go back and  enter the name of your product",400)
        if not request.form.get("quantity"):
            return apology("Please Input the quantity available")
        if not request.form.get("price"):
            return apology("Please Input the price of the product")
        if not request.form.get("description"):
            return apology("Please Input a short description of the product")
      #  if not request.form.get("picturename"):
       #     return apology("Please upload an image")
        filename = photos.save(request.files['photo'])

        firstname = request.form.get("firstname")
        #print (firstname)
        lastname = request.form.get("lastname")
        phonenumber = request.form.get("phonenumber") 
        phonenumber2 = request.form.get("phonenumber2") 
        location = request.form.get("location") 
        quantity = request.form.get("quantity") 
        price = request.form.get("price")
        product = request.form.get("product")
        category = request.form.get("category") 
        description = request.form.get("description") 
        image = filename 
        print (image)
     #  session["user_id"]       
        farmerid = sessionid
        date= datetime.date.today()
        #print(id)
        update_sell(firstname,lastname,phonenumber,phonenumber2,location,quantity,price,product,description,farmerid,date,image,category,our)
        return redirect("/farmers")


####### this route is to update data into rthe db
@app.route('/updatein',methods=['POST'])
def updatein():
    if request.method =='POST':
        print("i am here")
        idn = request.form.get("de")
        session["identify"] = idn
        pitch = get_investment("*","investment","id",idn)
        return render_template("updatepitch.html",pitch=pitch)

@app.route('/updatepitch',methods=['POST'])
def updatepitch():
    sessionid = session.get("user_id")
    idn = session.get("identify")
    if request.method=="POST"  and 'photo' in request.files:
        if not request.form.get("firstname"):
            return  apology(" Go back and  enter your first name",400)
        if not request.form.get("lastname"):
            return apology(" Please go back and enter your last name ",400)
        if not request.form.get("phonenumber"):
            return apology("Go back and  enter your phone number",400)
        if not request.form.get("category"):
            return apology("Go back and  specify the category of farm you run",400)
        if not request.form.get("location"):
            return apology("Error  Go back and  enter the location of your farm",400)
        # if not request.form.get("picturename"):
        #     return apology("Please Input a sample picture of your farm land")
        if not request.form.get("interest"):
            return apology("Please Input the interest rate to be earned by investor")
        if not request.form.get("description"):
            return apology("Please Input a short description of your business in view")
        firstname = request.form.get("firstname")
        #print (firstname)
        lastname = request.form.get("lastname")
        phonenumber = request.form.get("phonenumber") 
        phonenumber2 = request.form.get("phonenumber2") 
        category = request.form.get("category") 
        location = request.form.get("location") 
        fundneeded = request.form.get("fundneeded") 
        filename = photos.save(request.files['photo'])
        if filename:
            image = filename
        else:
            image = request.form.get ("photo")
        interest = request.form.get("interest") 
        #print(interest)
        farmerid = sessionid
        date= datetime.date.today()
        print(date)
        description = request.form.get("description") 
        title = request.form.get("title")
        pitch = get_investment("*","investment","id",farmerid)
        val=idn
        print(val)
        #print (title)
        update_invest(firstname,lastname,phonenumber,phonenumber2,category,location,fundneeded,image,interest,description,title,farmerid,date,val)
        #farmers = get_posts("*", "farmers", "id", farmerid)
        return redirect("/farmers")    

##############this route is for signup for as a user or farmer
@app.route('/signup',methods=['GET', 'POST'])
def signup():
    #wipe any users id
    session.clear()
    if request.method == 'POST'  and 'photo' in request.files:
        if not request.form.get("firstname"):
            return  apology(" Go back and  enter your first name",400)
        if not request.form.get("lastname"):
            return apology(" Please go back and enter your last name ",400)
        if not request.form.get("email"):
            return apology("Go back and  enter your email",400)
        if not request.form.get("phonenumber"):
            return apology("Go back and  enter your phone number",400)
        if not request.form.get("password"):
            return apology("Error  Go back and  enter your password",400)
        if request.form.get("password") != request.form.get("cpassword"):
            return apology("Password does not match",400)
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email= request.form.get("email")
        phonenumber = request.form.get("phonenumber")
        filename = photos.save(request.files['photo'])
        image = filename 
        print(image)
        password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        # password = hashs
        checkbox = request.form.get("farmer")
        if  len(get_posts("*","users","email",email)) or len(get_posts("*","farmers","email",email)) == 1:
            return  apology("A User already has this email",400)
        
        if checkbox == "farmer":
             create_post(firstname, lastname,email,phonenumber,password,checkbox,image)
        else:
             create_post(firstname, lastname,email,phonenumber,password,checkbox,image)

    # posts = get_posts()

        return render_template("success.html")#, posts = posts)
    else:
        return render_template('apology.html')

# @app.route('/',methods=['GET','POST'])
# def user():
#     if request.method == 


##### this is for login on other pages
@app.route('/investlogin',methods=['GET'])
def investlogin():
    return render_template("investlogin.html")

#######regular login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide username", 400)
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        email = request.form.get("email")
        #print(email)
        password = request.form.get("password")
        #print(password)
        # Query database for username
        rows =get_posts("*","users","email",email) #db.execute("SELECT * FROM users WHERE username = :username",
       # print(rows)
        rows1 =get_posts("*","farmers","email",email) #db.execute("SELECT * FROM users WHERE username = :username",
        #print(rows1)
                         # username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 and len(rows1) != 1:
            return apology("invalid username", 400)
        if len(rows) ==1 and not check_password_hash(rows[0][4], request.form.get("password")):
            return apology("invalid password", 400)
        elif len(rows1) ==1 and not check_password_hash(rows1[0][4], request.form.get("password")):
            return apology("invalid passowrd", 400)

        # Remember which user has logged in
        if len(rows1)==0:
            session["user_id"] = rows[0][0]
            
            
            return redirect("/users")
        elif len(rows1)==1:
            session["user_id"] = rows1[0][0]
            ddd = session.get("user_id")
            print(ddd)
            return redirect("/farmers")

        # Redirect user to home page
       # return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


############getting farmers details
@app.route("/farmers",methods=["GET"])
@login_required
def farmers():
    """Show farmers details"""
    id = session["user_id"]
    farmers = get_posts("*", "farmers", "id", id)
    session["email"] = farmers[0][3]
    sell = get_sell("*","sell","farmerid",id)
    investment =get_investment("*","investment","farmerid",id)
    return render_template("farmers.html",farmers=farmers,sell=sell,investment=investment)

    ####### route to click and redirect to profile from anywhere on the page
@app.route("/profile",methods=["GET"])
def profile():
    """Show farmers details"""
    trackingid = session.get("user_id")
    emailid =session.get("email")
    print (emailid)
    farmers = get_posts("*", "farmers", "id", trackingid)
    print(farmers)
    users = get_posts("*", "users", "id", trackingid)
    print(users)
    print("farmers are great")
    if len(farmers)==1 and farmers[0][3] == emailid:
        return redirect("/farmers")
    elif len(users)==1 and users[0][3]==emailid:
        return redirect("/users")

###################route for farmers to pitch  their ideas for investment
@app.route("/pitch",methods=["GET","POST"])
#@login_required
def pitch():
    sessionid = session.get("user_id")
    print(sessionid)
    """Show farmers details"""
    if request.method=="GET":
        #id = session["user_id"]
        #farmers = get_posts("*", "farmers", "id", id)
        return render_template("pitch.html")
    if request.method=="POST"  and 'photo' in request.files:
        if not request.form.get("firstname"):
            return  apology(" Go back and  enter your first name",400)
        if not request.form.get("lastname"):
            return apology(" Please go back and enter your last name ",400)
        if not request.form.get("phonenumber"):
            return apology("Go back and  enter your phone number",400)
        if not request.form.get("category"):
            return apology("Go back and  specify the category of farm you run",400)
        if not request.form.get("location"):
            return apology("Error  Go back and  enter the location of your farm",400)
        # if not request.form.get("picturename"):
        #     return apology("Please Input a sample picture of your farm land")
        if not request.form.get("interest"):
            return apology("Please Input the interest rate to be earned by investor")
        if not request.form.get("description"):
            return apology("Please Input a short description of your business in view")
        firstname = request.form.get("firstname")
        #print (firstname)
        lastname = request.form.get("lastname")
        phonenumber = request.form.get("phonenumber") 
        phonenumber2 = request.form.get("phonenumber2") 
        category = request.form.get("category") 
        location = request.form.get("location") 
        fundneeded = request.form.get("fundneeded") 
        filename = photos.save(request.files['photo'])
        image = filename 
        interest = request.form.get("interest") 
        #print(interest)
        farmerid = sessionid
        date= datetime.date.today()
        print(date)
        description = request.form.get("description") 
        title = request.form.get("title")
        #print (title)
        if  len(get_investment("*","investment","title",title))== 1:
            return  apology("you already pitched this investment",400)
        create_invest(firstname,lastname,phonenumber,phonenumber2,category,location,fundneeded,image,interest,description,title,farmerid,date)
    return render_template("success1.html")
    

#################route for uploading items to be sold into db
@app.route("/sell",methods=["GET","POST"])
#@login_required
def sell():
    """Show farmers details"""
    sessionid = session.get("user_id")
    print(sessionid)
    if request.method=="GET":
        #id = session["user_id"]
        #farmers = get_posts("*", "farmers", "id", id)
        return render_template("sell.html")
    if request.method=="POST" and 'photo' in request.files:
        if not request.form.get("firstname"):
            return  apology(" Go back and  enter your first name",400)
        if not request.form.get("category"):
            return apology("Go back and  specify the category of farm you run",400)
        if not request.form.get("lastname"):
            return apology(" Please go back and enter your last name ",400)
        if not request.form.get("phonenumber"):
            return apology("Go back and  enter your phone number",400)
        if not request.form.get("location"):
            return apology("Error  Go back and  enter the location of your farm",400)
        if not request.form.get("product"):
            return apology("Error  Go back and  enter the name of your product",400)
        if not request.form.get("quantity"):
            return apology("Please Input the quantity available")
        if not request.form.get("price"):
            return apology("Please Input the price of the product")
        if not request.form.get("description"):
            return apology("Please Input a short description of the product")
      #  if not request.form.get("picturename"):
       #     return apology("Please upload an image")
        filename = photos.save(request.files['photo'])

        firstname = request.form.get("firstname")
        #print (firstname)
        lastname = request.form.get("lastname")
        phonenumber = request.form.get("phonenumber") 
        phonenumber2 = request.form.get("phonenumber2") 
        location = request.form.get("location") 
        quantity = request.form.get("quantity") 
        price = request.form.get("price")
        product = request.form.get("product")
        category = request.form.get("category") 
        description = request.form.get("description") 
        image = filename 
        print (image)
     #  session["user_id"]       
        farmerid = sessionid
        date= datetime.date.today()
        #print(id)
 
        if  len(get_sell("*","sell","product",product))== 1:
            return  apology("you already have this for sale",400)
        create_sell(firstname,lastname,phonenumber,phonenumber2,location,quantity,price,product,description,farmerid,date,image,category)
    return render_template("success1.html")

############route for populating the buy page
@app.route("/buy", methods=["GET"])
def buy():
    """Show history of transactions"""
    # if request.method=="GET":
    #     row3 = get_sell2("*","sell")
    #     return render_template("buy.html",row3=row3)
    if request.method=="GET":
        row3 = get_sell2("*","sell")
    arable =[]
    livestock = []
    for row in row3:
        if row[13] == "Arable":
            arable.append(row)
        if row[13] == "livestock":
            livestock.append(row)
    print(arable)
    print(livestock)
    return render_template("buy.html",livestock=livestock,arable=arable)

####### route to populate the invetment page
@app.route("/invest", methods=["GET"])
def investment():
    """Show history of transactions"""
    if request.method=="GET":
        row3 = get_sell2("*","investment")
    arable =[]
    livestock = []
    for row in row3:
        if row[4] == "Arable":
            arable.append(row)
        if row[4] == "livestock":
            livestock.append(row)
    print(arable)
    print(livestock)
    return render_template("invest.html",livestock=livestock,arable=arable)
        #return render_template("invest.html",row3=row3)




############getting users details
@app.route("/users",methods=["GET"])
@login_required
def users():
    """Show farmers details"""
    id = session["user_id"]
    users = get_posts("*", "users", "id", id)
    session["email"] = users[0][3]
    return render_template("user.html",users=users)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == '__main__':
    app.run(debug=True)

