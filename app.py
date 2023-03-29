from flask import Flask,redirect,request,url_for,render_template,session
import smtplib
import random

s= smtplib.SMTP('smtp.gmail.com',587)
s.starttls()

s.login("obulasaimochi@gmail.com","eqhdlixqglrmynjo")
app = Flask(__name__)

import pymysql.cursors
con = pymysql.connect(host='sql12.freemysqlhosting.net',
                      user='sql12609212',
                      password='U4IDdjVfNY',
                      database='sql12609212'
                      )
cursor = con.cursor()
app.secret_key="qwerty"


@app.route('/',methods=['GET','POST'])
def home():

        if("user" in session):
            return render_template("index.html")
        else:
            return redirect('/login')




@app.route('/login',methods=['POST','GET'])
def login():
    if(request.method=='POST'):
        session.permanent=True
        email = request.form['email-l']
        session['user'] = email
        password = request.form['password-l']
        l1=[]
        emails=[]
        sql="select email from customers"
        cursor.execute(sql)
        var1 = cursor.fetchall()
        for i in var1:
            l1.append(i)
        for i in l1:
            for j in i:
                emails.append(str(j))
        
        if(email in emails):
            sql = "select password from customers where email=(%s)"
            v = [email]
            cursor.execute(sql,v)
            var = cursor.fetchone()
            password1 = var[0]
            if(password==password1):
                return render_template('index.html')
            else:
                msg="incorrect password !"
                return render_template("login.html",msg=msg)
        else:
            msg="you have no account please create a new account !"
            return render_template("login.html",msg=msg)



    return render_template("login.html")


@app.route('/logout')
def lagout():
    session.pop("user",None)
    return redirect('/login')


@app.route('/register',methods=['POST','GET'])
def register():
    if(request.method=='POST'):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        email = str(email)
        l1=[]
        emails=[]
        sql="select email from customers"
        cursor.execute(sql)
        var1 = cursor.fetchall()
        for i in var1:
            l1.append(i)
        for i in l1:
            for j in i:
                emails.append(str(j))
        if(email in emails):
            msg="you have already account please login !"
            return render_template('register.html',msg=msg)
        else:
            sql = "insert into customers(username,email,password)values(%s,%s,%s)"
            l = [name,email,password]
            cursor.execute(sql,l)
            con.commit()
            return redirect('/')
    return render_template("register.html")






@app.route('/forgetpassword',methods=['POST','GET'])
def forgetpassword():
    if(request.method=='POST'):
        email = request.form['email-f']
        session['user'] = email
        otp = request.form['otp']
        otp = str(otp)
        # s1=5436
        # s1=str(s1)
        list=[1,2,3,4,5,6,7,8,9,0]
        s1=""
        for i in range(4):
            s1+=str(random.choice(list))
        
        if(len(otp)==0):

            msg = "your otp for verification is {}".format(s1)
            session['s1'] = s1
            s.sendmail("obulasaimochi@gmail.com",email,msg)
            s.quit()
            return render_template("forgetpassword.html",msg="OTP sent!")
        else:
            if(otp == session['s1']):
                return redirect("/createpassword")
            else:
                m="OTP does'not match"
                return render_template("forgetpassword.html",msg=m)

    return render_template("forgetpassword.html")


@app.route('/createpassword',methods=['POST','GET'])
def createpass():
    if "user" in session:
        if(request.method=='POST'):
            email = session['email']
            password = request.form['pass']
            passc = request.form['pass-c']
            password=str(password)
            email=str(email)
            if(password == passc):
                sql = "update `customers` set `password`=(%s) where `email` =(%s)"
                v=[password,email]
                cursor.execute(sql,v)
                con.commit()
                return redirect("/login")
            else:
                return render_template("createpass.html",msg="passwords not matched !")
        return render_template("createpass.html")
    else:
        return redirect("/login")





@app.route('/<p>',methods=['POST','GET'])
def tshirt(p):
    if "user" in session:
        user = session['user']
        product=p
        list=[user,product]
        sql = "insert into carts(cname,pname)values(%s,%s)"
        cursor.execute(sql,list)
        con.commit()
        return redirect('/cart')
    else:
        return redirect('/login')




@app.route('/cart')
def cart():
    if "user" in session:
        user = session['user']
        products=[]
        sql = "select * from carts where cname=(%s)"
        cursor.execute(sql,user)
        var = cursor.fetchall()
        for i in var:
            products.append(i[1])

        list1=[]
        for i in products:
            sql1="select * from products where pname=(%s)"
            cursor.execute(sql1,i)
            var1 = cursor.fetchall()
            for i in var1:
                list1.append(list(i))

        return render_template("cart.html",pdts=list1)
    else:
        return redirect('/login')


con.commit()



if __name__ == "__main__":
    app.run(debug=True)

























