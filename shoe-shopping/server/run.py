from typing import Literal
from flask import Flask, flash,render_template,redirect,session,request, url_for
from flaskext.mysql import MySQL 
# Date time
from datetime import date
#date add 15 days interval
from sqlalchemy import Table, Column, MetaData, DateTime
from datetime import datetime, timedelta
# validation--not needed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf
# Base64
from PIL import Image
from io import BytesIO
import base64
#mail
from flask_mail import Mail, Message
import smtplib

from pymysql import NULL

app = Flask(__name__)

# create db connection

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'maneesha@176'
app.config['MYSQL_DATABASE_DB'] = 'ecom'
mysql = MySQL(app)
mysql.init_app(app)

#mail
mail = Mail(app) # instantiate the mail class

   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shoeshoppi1101@gmail.com'
app.config['MAIL_PASSWORD'] = 'abcd1101'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
   


#Login & Registration 

# @app.route('/login', methods=['GET','POST'])
# def do_admin_login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     if request.method=='POST':
#         conn =mysql.connect()
#         cursor = conn.cursor()
#         query="SELECT * FROM ecom.login where username=%s and password=%s"
#         cursor.execute(query,(request.form['username'],request.form['password']))
#         conn.commit()
#         account=cursor.fetchone()
#         if account:
#             print(account)
#          #   session['loggedin'] =True
#             session['username']= account[1] 
#             session['id']= account[4]  
#             session['type']= account[3]
#             if (account[3] == 'user'):
#                 return redirect(url_for('index-user'))
#             elif (account[3] == 'admin'):
#                 return redirect(url_for('index-admin'))                                                          
            
            
#    # #  if request.form['password'] == 'password' and request.form['username'] == 'admin':
#    #      session['logged_in'] = True
#    #  else:
#    #      flash('wrong password!')
#    #  return redirect(url_for('do_admin_login'))    

# # @app.route('/logout', methods=['GET'])
# # def test():
# #     if session['loggedin']:
# #         session['loggedin']=False
# #         session.pop('id',None)
# #         session.pop('username',None)
# #         return redirect(url_for('do_admin_login'))
# #     else:
# #         print("login first")  

#Login

@app.route('/login', methods=['GET','POST'])
def do_login():
    if request.method == 'GET':    
        return render_template('login.html')
    if request.method=='POST':
        conn =mysql.connect()
        cursor = conn.cursor()
        query="select * from login where username=%s and password=%s"
        cursor.execute(query,(request.form['username'],request.form['password']))
        conn.commit()
        account=cursor.fetchone()
        if account:
            print(account)
            session['loggedin'] =True
            session['username']= account[1]                  
            session['uid']= account[4]
            session['type']= account[3]
            if (account[3] == 'user'):
                return redirect(url_for('user'))
            elif (account[3] == 'admin'):
                return redirect(url_for('admin'))
            elif (account[3] == 'brandowner'):
                return redirect(url_for('brandowner'))
              
#        #if request.form['password'] == 'password' and request.form['username'] == 'admin':
#           session['logged_in'] = True
#        else:
#         flash('wrong password!')           
    return redirect(url_for('do_login'))

         
@app.route('/logout',methods=['GET'])
def logout():
   if session['loggedin']:
      session['loggedin']=False
      session.pop('id',None)
      session.pop('username',None)
      return redirect(url_for('login'))
   else:   
      print("login first")


#Registration

# @app.route('/registration', methods=['GET', 'POST'])
# def registration():
#         if request.method == 'GET':
#             return render_template("registration.html")
#         if request.method == 'POST':
#             data = request.form
#             conn = mysql.connect()
#             cursor = conn.cursor()
#             query = "INSERT INTO user(username,phn,email,house_name,street,city,zipcode) VALUES(%s,%s,%s,%s,%s,%s,%s)"
#             cursor.execute(query, (data['username'], data['phn'], data['email'], data['house_name'], data['street'], data['city'], data['zipcode']))
#             print(query)
#             conn.commit()
#             query = "insert into login(username,password,type,uid) values (%s,%s,%s,%s)"
#             cursor.execute(query, (data['email'], data['password'], 'user', cursor.lastrowid))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('registration'))

#User Registration

@app.route('/registration',methods=['GET','POST'])
def registration():    
      if request.method == 'GET':
          return render_template('registration.html')
      if request.method == 'POST':
            data = request.form
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "INSERT INTO user(username,phn,email,house_name,street,city,zipcode) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query, (data['username'], data['phn'], data['email'], data['HouseName'], data['Street'], data['City'], data['zipcode']))
            print(query)
            conn.commit()
            query = "insert into login(username,password,type,uid) values (%s,%s,%s,%s)"
             # INSERT INTO login(id,username,password,type,uid) VALUES(1,'admin','admin','admin',1);
            cursor.execute(query, (data['email'], data['password'], 'user', cursor.lastrowid))
            conn.commit()
            conn.close()
            return redirect(url_for('registration'))


 ##Main Page=================================
@app.route('/')
def index():
   return render_template('index-main.html')

@app.route('/view-shoes')
def viewshoes():
   return render_template('view-shoes.html')

@app.route('/aboutus')
def aboutus():
   return render_template('aboutus.html')   

##USER SIDE=============================

@app.route('/user')
def user():
   return render_template('index-user.html') 

@app.route('/about')
def about():
   return render_template('about.html') 

@app.route('/contact')
def contact():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM category"
   cursor.execute(query)
   category=cursor.fetchall()
   conn.commit()
   conn.close()
# -------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM color"
   cursor.execute(query)
   color=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM brand"
   cursor.execute(query)
   brand=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM type"
   cursor.execute(query)
   type=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM size"
   cursor.execute(query)
   size=cursor.fetchall()
   conn.commit()
   conn.close()

# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM shoes"
   cursor.execute(query)
   shoes=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   return render_template('contact.html',category=category,brand=brand,type=type,color=color,size=size,shoes=shoes) 
# ------------------------------------------------------------------------------------------------>

# ------------------------------------------------------------------------------------------------>
@app.route('/addcart',methods=['GET','POST'])
def addcart():
   if request.method == 'POST':
      data = request.form
      conn = mysql.connect()
      cursor = conn.cursor()
      query ="insert into cart (p_id,quantity,u_id,total) values(%s,%s,%s,%s)" 
      cursor.execute(query, ( data['pid'], data['quantity'],session['uid'], data['total']))
      conn.commit()
      conn.close()
      return redirect(url_for('cart'))

# @app.route('/updatecart',methods=['GET','POST'])
# def updatecart():
#    if request.method == 'POST':
#       data = request.form
#       conn = mysql.connect()
#       cursor = conn.cursor()
#       query ="update ecom.cart set quantity=%s,total=%s where ca_id =%s" 
#       cursor.execute(query, ( data['quantity'], data['total'], data['caid']))
#       conn.commit()
#       conn.close()
#       return redirect(url_for('cart'))
   
#------------------------------------------------------------->

#------------------------------------------------------------->  
@app.route('/cart')
def cart():
   conn = mysql.connect()
   cursor = conn.cursor()
   query="SELECT * FROM ecom.cart,ecom.shoes where cart.p_id=shoes.p_id and u_id=%s"
   cursor.execute(query, ( session['uid']))
   cart=cursor.fetchall()
   conn.commit()
   query="select count(ca_id) from ecom.cart where u_id=%s"
   cursor.execute(query, ( session['uid']))
   cartno=cursor.fetchall()
   conn.commit()
   query="select sum(total) from cart where u_id=%s"
   cursor.execute(query, ( session['uid']))
   sum=cursor.fetchall()
   return render_template('cart.html',cart=cart,cartno=cartno,sum=sum,) 
#------------------------------------------------------------->

#------------------------------------------------------------->  
@app.route('/orderitems')
def orderitems():
   today = date.today()
   conn = mysql.connect()
   cursor = conn.cursor()
   query="select sum(total) from cart where u_id=%s"
   cursor.execute(query, ( session['uid']))
   total=cursor.fetchall()
   conn.commit()
   # --------------------------------------
   query="insert into orders(date,total_rate,user_id,approval_status,delivery_status) values(%s,%s,%s,%s,%s)"
   cursor.execute(query, ( today, total, session['uid'], 'pending', 'pending'))
   conn.commit()
   # --------------------------------------
   query="select max(o_id) from orders"
   cursor.execute(query)
   oid=cursor.fetchall()
   conn.commit()
   # --------------------------------------
   query="insert into ordered_items(pid,quantity,sub_total,o_id) select p_id,quantity,total,%s from cart where u_id=%s"
   cursor.execute(query, ( oid, session['uid']))
   conn.commit()
   # --------------------------------------
   query="delete FROM ecom.cart where u_id=%s"
   cursor.execute(query, ( session['uid']))
   conn.commit()
# insert into ordered_items(pid,quantity,sub_total,o_id) select p_id,quantity,total,1 from cart where u_id=1
# delete * from cart where uid=1
#orders
#select * from order where delivery status = delivered -->order history
#select * from order where delivery status != delivered --->current order(only one at a time)
#select delivery status where delivery status !=delivered if !=0 the order is not possible
   return redirect(url_for('cart'))
#------------------------------------------------------------->

#------------------------------------------------------------->     

@app.route('/men')
def men():
   return render_template('men.html') 
  #------------------------------------------------------------->

#------------------------------------------------------------->   
@app.route('/Shoes')
def Shoes():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM category"
   cursor.execute(query)
   category=cursor.fetchall()
   conn.commit()
   conn.close()
# -------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM color"
   cursor.execute(query)
   color=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM brand"
   cursor.execute(query)
   brand=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM type"
   cursor.execute(query)
   type=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM size"
   cursor.execute(query)
   size=cursor.fetchall()
   conn.commit()
   conn.close()

# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM shoes"
   cursor.execute(query)
   shoes=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('Shoes.html',category=category,color=color,brand=brand,type=type,size=size,shoes=shoes)
#------------------------------------------------------------->

#------------------------------------------------------------->    
@app.route('/product-detail')
def productDetail():
   id = request.args.get('id')
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM shoes where p_id=%s"
   cursor.execute(query, (id))
   shoes=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT color FROM color where co_id=(SELECT co_id FROM shoes where p_id=%s)"
   cursor.execute(query, (id))
   color=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT size FROM size where s_id=(SELECT s_id FROM shoes where p_id=%s)"
   cursor.execute(query, (id))
   size=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT category FROM category where c_id=(SELECT c_id FROM shoes where p_id=%s)"
   cursor.execute(query, (id))
   category=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT brand FROM brand where b_id=(SELECT b_id FROM shoes where p_id=%s)"
   cursor.execute(query, (id))
   brand=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT type FROM type where t_id=(SELECT t_id FROM shoes where p_id=%s)"
   cursor.execute(query, (id))
   type=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('product-detail.html',shoes=shoes,color=color,size=size,category=category,brand=brand,type=type,id=id)  
 #------------------------------------------------------------->

 #------------------------------------------------------------->     
@app.route('/order-complete')
def ordercomplete():
   return render_template('order-complete.html') 
      
@app.route('/add-to-wishlist')
def addtowishlist():
   return render_template('add-to-wishlist.html')    

      
@app.route('/checkout')
def checkout():
   return render_template('checkout.html') 

 #------------------------------------------------------------->

#------------------------------------------------------------->  
@app.route('/orders')
def orders():
   conn = mysql.connect()
   cursor = conn.cursor()
   # query = "SELECT * FROM ordered_items where o_id in (SELECT o_id FROM orders where user_id=%s and delivery_status !='delivered')"
   query = "SELECT o_id FROM orders where user_id=%s and delivery_status !='delivered'"
   cursor.execute(query, (session['uid']))
   oid=cursor.fetchall()
   conn.commit()
   # --------------------------------------
   query = "SELECT * FROM ordered_items,shoes where ordered_items.pid=shoes.p_id and o_id=%s"
   cursor.execute(query, (oid))
   orders=cursor.fetchall()
   conn.commit()
   # --------------------------------------
   query = "SELECT * FROM orders where user_id=%s and delivery_status !='delivered'"
   cursor.execute(query, (session['uid']))
   status=cursor.fetchall()
   conn.commit()
   # --------------------------------------
   query="select count(oi_id) FROM ordered_items,shoes where ordered_items.pid=shoes.p_id and o_id=%s"
   cursor.execute(query, (oid))
   orderno=cursor.fetchall()
   conn.commit()
   # --------------------------------------
   query="select sum(sub_total) FROM ordered_items,shoes where ordered_items.pid=shoes.p_id and o_id=%s"
   cursor.execute(query, (oid))
   sum=cursor.fetchall()
   conn.commit()
   # --------------------------------------
   query = "SELECT o_id FROM orders where user_id=%s"
   cursor.execute(query, (session['uid']))
   oidsecond=cursor.fetchall()
   conn.commit()
   #--------------------------------------
   query = "SELECT * FROM orders,ordered_items,shoes where ordered_items.pid=shoes.p_id and orders.o_id=ordered_items.o_id and orders.user_id=%s and orders.delivery_status='delivered';"
   cursor.execute(query, (session['uid']))
   history=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('orders.html',orders=orders,orderno=orderno,sum=sum,status=status,history=history) 

   
 # ---------------------------------------------------------->

 # ---------------------------------------------------------->
@app.route('/profile')
def profile():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from user where uid=%s"
   cursor.execute(query, (session['uid']))
   profile=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('profile.html',profile=profile) 
 # ---------------------------------------------------------->
@app.route('/editprofile',methods=['GET','POST'])
def editprofile():
   conn = mysql.connect()
   cursor = conn.cursor()
   data=request.form
   query = "UPDATE user SET  username=%s, phn=%s, email=%s, house_name=%s, street=%s, city=%s, zipcode=%s WHERE uid=%s"
   cursor.execute(query, ( data['username'], data['phone'], data['email'], data['house'], data['street'], data['city'], data['zip'], session['uid']))
   conn.commit()
   query = "UPDATE login SET  username=%s WHERE uid=%s"
   cursor.execute(query, ( data['email'], session['uid']))
   conn.commit()
   query = "select * from user where uid=%s"
   cursor.execute(query, (session['uid']))
   profile=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('profile.html',profile=profile) 
 # ---------------------------------------------------------->

  # ---------------------------------------------------------->
#Sent Feedback about site
@app.route("/contactadmin",methods=['GET','POST'])
def contactadmin():
  if request.method == 'POST':
   conn = mysql.connect()
   cursor = conn.cursor()
   subject=request.form.get("subject")
   message=request.form.get("message")
   uid=session['uid']
   query = "insert into feedback(subject,feedback,u_id) values (%s,%s,%s)"
   cursor.execute(query, (subject,message,uid))
   conn.commit()
   conn.close()
   return redirect(url_for('contact'))


#Sent Feedback about product
@app.route("/product-issue",methods=['GET','POST'])
def productIssue():
   if request.method == 'POST':
      conn = mysql.connect()
      cursor = conn.cursor()
      data=request.form
      uid=session['uid']
      today = date.today()
      query = "select p_id from shoes where c_id=%s and b_id=%s and t_id=%s and co_id=%s and s_id=%s"
      cursor.execute(query, (data['category'], data['brand'], data['type'], data['color'], data['size']))
      pid=cursor.fetchall()
      cursor.close()
      conn.close()
      #If The Length Of An Array Pid > 0 run the following code.
      if (len(pid)>0):
         conn = mysql.connect()
         cursor = conn.cursor()
         print(pid)
         query = "insert into complaints (u_id,p_id,subject,complaint,date) values(%s,%s,%s,%s,%s)"
         cursor.execute(query, (uid, pid, data['subject'], data['complaint'], today))
         conn.commit()
         conn.close()
         flash("The Complaint Is Registered.")
         return redirect(url_for('contact'))
      else :
         flash("The Shoe Does Not Exist!")  
   return redirect(url_for('contact'))

         

##=======================ADMIN SIDE====================================================
##====##====##====##====##====##====##====##====##====##====##====##====##====##====

@app.route('/admin')
def admin():
   return render_template('index-admin.html')    


@app.route('/feedback')
def feedback():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT username FROM user where uid=1;"
   cursor.execute(query)
   username=cursor.fetchall()
   conn.commit()
   query = "select * from feedback"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   query = "SELECT * FROM complaints,user,shoes where complaints.u_id=user.uid and shoes.p_id=complaints.p_id"
   cursor.execute(query)
   complaints=cursor.fetchall()
   conn.close()
   return render_template('feedback.html',data=data,username=username,complaints=complaints)    



@app.route('/deletefeedback')
def delfeedback():
   fid = request.args.get('fid')
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "delete from feedback where f_id=%s"
   cursor.execute(query ,(fid))
   conn.commit()
   conn.close()
   return redirect(url_for('feedback'))   


@app.route('/deletecomplaint')
def delcomp():
   comid = request.args.get('comid')
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "delete from complaints where com_id=%s"
   cursor.execute(query ,(comid))
   conn.commit()
   conn.close()
   return redirect(url_for('feedback'))   

@app.route('/view-orders')
def vieworders():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM ecom.orders,ecom.user where orders.user_id=user.uid and delivery_status!='delivered';"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('view-orders.html',data=data) 

@app.route('/orders-admin',methods=['GET','POST'])
def OrdersAdmin():
   oid = request.args.get('oid')
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM ecom.orders,ecom.ordered_items,ecom.shoes where orders.o_id=%s and orders.o_id=ordered_items.o_id and ordered_items.pid=shoes.p_id"
   cursor.execute(query,(oid))
   data=cursor.fetchall()
   conn.commit()
   query = "select distinct date,total_rate from ecom.orders where o_id=%s"
   cursor.execute(query,(oid))
   datas=cursor.fetchall()
   conn.commit()
   query = "select count(oi_id) from ecom.ordered_items where o_id=%s"
   cursor.execute(query,(oid))
   count=cursor.fetchall()
   conn.commit()
   query = "select approval_status,delivery_status from ecom.orders where o_id=%s"
   cursor.execute(query,(oid))
   status=cursor.fetchall()
   conn.commit()
   # query = "select date from ecom.orders where o_id=%s"
   # cursor.execute(query,(oid))
   # date=cursor.fetchall()
   # expected=date+10
   # conn.commit()
   conn.close()
   return render_template('Orders-admin.html',data=data,datas=datas,count=count,status=status,date=date)  

@app.route('/manage-order',methods=['GET','POST'])
def manageorder():
   conn = mysql.connect()
   cursor = conn.cursor()
   data=request.form
   approval=data['approval']
   query = "UPDATE orders SET  approval_status=%s, delivery_status=%s where o_id=%s"
   cursor.execute(query, ( data['approval'], data['delivery'], data['oid']))
   conn.commit()
   if approval=='canceled':
      query = "UPDATE orders SET delivery_status=%s where o_id=%s"
      cursor.execute(query, ( 'pending', data['oid']))
      conn.commit()
      conn.close()
      return redirect(url_for('vieworders'))
   else :
      conn.close()
   return redirect(url_for('vieworders'))

@app.route('/users')
def viewusers():
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "select * from user"
    cursor.execute(query)
    data=cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template('view-users.html',data=data)
@app.route('/deleteusers')
def deleteuser():
   uid = request.args.get('uid')
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "delete from login where uid=%s"
   cursor.execute(query ,(uid))
   conn.commit()
   query = "delete from user where uid=%s"
   cursor.execute(query ,(uid))
   conn.commit()
   query = "delete from cart where u_id=%s"
   cursor.execute(query ,(uid))
   conn.commit()
   query = "delete from complaints where u_id=%s"
   cursor.execute(query ,(uid))
   conn.commit()
   query = "delete from feedback where u_id=%s"
   cursor.execute(query ,(uid))
   conn.commit()
   query = "delete from orders where user_id=%s"
   cursor.execute(query ,(uid))
   conn.commit()
   conn.close()
   return redirect(url_for('viewusers'))
#------------------------------------------------------------->
#------------------------------------------------------------->
@app.route('/shoes-admin')
def shoesadmin():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM category"
   cursor.execute(query)
   category=cursor.fetchall()
   conn.commit()
   conn.close()
# -------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM color"
   cursor.execute(query)
   color=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM brand"
   cursor.execute(query)
   brand=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM type"
   cursor.execute(query)
   type=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM size"
   cursor.execute(query)
   size=cursor.fetchall()
   conn.commit()
   conn.close()

# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM shoes"
   cursor.execute(query)
   shoes=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('shoes-admin.html',category=category,color=color,brand=brand,type=type,size=size,shoes=shoes)
#------------------------------------------------------------->

#ADD Shoes 
@app.route("/addshoes",methods=['GET','POST'])
def addshoes():
  if request.method == 'POST':
   conn = mysql.connect()
   cursor = conn.cursor()
   data=request.form
   img = request.files['file']  
   file = base64.b64encode(img.read())
   query = "insert into ecom.shoes(img, shoe, description, c_id, b_id, t_id, co_id, s_id, price, avalability) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
   cursor.execute(query, (file, data['Shoe'], data['description'], data['category'], data['brand'], data['type'], data['color'], data['size'], data['rate'], data['availability']))
   conn.commit()
   conn.close()
#----------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM category"
   cursor.execute(query)
   category=cursor.fetchall()
   conn.commit()
   conn.close()
# -------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM color"
   cursor.execute(query)
   color=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM brand"
   cursor.execute(query)
   brand=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM type"
   cursor.execute(query)
   type=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM size"
   cursor.execute(query)
   size=cursor.fetchall()
   conn.commit()
   conn.close()

# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM shoes"
   cursor.execute(query)
   shoes=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('shoes-admin.html',category=category,color=color,brand=brand,type=type,size=size,shoes=shoes)
#------------------------------------------------------------->
#------------------------------------------------------------->
@app.route('/product-details')
def productDetails():
   id = request.args.get('id')
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM shoes where p_id=%s"
   cursor.execute(query, (id))
   shoes=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT color FROM color where co_id=(SELECT co_id FROM shoes where p_id=%s)"
   cursor.execute(query, (id))
   color=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT size FROM size where s_id=(SELECT s_id FROM shoes where p_id=%s)"
   cursor.execute(query, (id))
   size=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT category FROM category where c_id=(SELECT c_id FROM shoes where p_id=%s)"
   cursor.execute(query, (id))
   category=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT brand FROM brand where b_id=(SELECT b_id FROM shoes where p_id=%s)"
   cursor.execute(query, (id))
   brand=cursor.fetchall()
   conn.commit()
   conn.close()
# --------------------------------------
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT type FROM type where t_id=(SELECT t_id FROM shoes where p_id=%s)"
   cursor.execute(query, (id))
   type=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('admin-product-details.html',shoes=shoes,color=color,size=size,category=category,brand=brand,type=type) 


@app.route('/manage')
def manage():
   return render_template('manage.html')


@app.route('/generate')
def generate():
   return render_template('Generate_login.html')
   
#mail
@app.route("/email",methods=['GET','POST'])
def email():
  if request.method == 'POST':
   conn = mysql.connect()
   cursor = conn.cursor()
   username=request.form.get("username")
   password=request.form.get("password")
   email=request.form.get("email")
   brand=request.form.get("brand")

   msg = Message(
                'Hello' ,
                sender ='shoeshoppi1101@gmail.com',
                recipients = [email]
               )
   msg.body = ' Hello, %s  Your password is  %s'%(username,password)
   mail.send(msg)
   #DB Operation
   query = "insert into login(username,password,type) values (%s,%s,%s)"
   cursor.execute(query, (email, password, 'brandowner'))
   conn.commit()
   conn.close()
   return redirect(url_for('generate'))

#Category form
@app.route("/category",methods=['GET','POST'])
def category():
  if request.method == 'POST':
   conn = mysql.connect()
   cursor = conn.cursor()
   category=request.form.get("category")
   query = "insert into category(category,type) values (%s,%s)"
   cursor.execute(query, (category,'category'))
   conn.commit()
   conn.close()
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from category"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-category.html',data=data)


# Category table
@app.route('/manage-category')
def categorytable():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from category"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-category.html',data=data)


#Brand form
@app.route("/brand",methods=['GET','POST'])
def brand():
  if request.method == 'POST':
   conn = mysql.connect()
   cursor = conn.cursor()
   brand=request.form.get("brand")
   query = "insert into brand(brand,type) values (%s,%s)"
   cursor.execute(query, (brand,'brand'))
   conn.commit()
   conn.close()
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from brand"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-brands.html',data=data)

# Brand table
@app.route('/manage-brand')
def brandtable():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from brand"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-brands.html',data=data)



#Type form
@app.route("/type",methods=['GET','POST'])
def type():
  if request.method == 'POST':
   conn = mysql.connect()
   cursor = conn.cursor()
   type=request.form.get("type")
   query = "insert into type(type,types) values (%s,%s)"
   cursor.execute(query, (type,'types'))
   conn.commit()
   conn.close()
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from type"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-type.html',data=data)

# Types table
@app.route('/manage-type')
def typetable():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from type"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-type.html',data=data)


#Color form
@app.route("/color",methods=['GET','POST'])
def color():
  if request.method == 'POST':
   conn = mysql.connect()
   cursor = conn.cursor()
   color=request.form.get("color")
   query = "insert into color(color,type) values (%s,%s)"
   cursor.execute(query, (color,'color'))
   conn.commit()
   conn.close()
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from color"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-color.html',data=data)

 #color table
@app.route('/manage-color')
def colortable():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from color"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-color.html',data=data)
  


#Size form
@app.route("/size",methods=['GET','POST'])
def size():
  if request.method == 'POST':
   conn = mysql.connect()
   cursor = conn.cursor()
   size=request.form.get("size")
   query = "insert into size(size,type) values (%s,%s)"
   cursor.execute(query, (size,'size'))
   conn.commit()
   conn.close()
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from size"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-size.html',data=data)
   
# Size table
@app.route('/manage-size')
def sizetable():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from size"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-size.html',data=data)

#Remove Size
@app.route("/removesize")
def removesize():
   conn = mysql.connect()
   cursor = conn.cursor()
   id = request.args.get('id')
   query = "DELETE FROM size WHERE s_id =%s"
   cursor.execute(query, (id))
   conn.commit()
   conn.close()
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "select * from size"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('manage-size.html',data=data)

###====================Brand Owner========================

@app.route('/brandowner')
def brandowner():
   return render_template('index-brandowner.html')    


@app.route('/complaints')
def complaints():
   conn = mysql.connect()
   cursor = conn.cursor()
   query = "SELECT * FROM complaints,user,shoes where complaints.u_id=user.uid and shoes.p_id=complaints.p_id"
   cursor.execute(query)
   data=cursor.fetchall()
   conn.commit()
   conn.close()
   return render_template('complaints.html',data=data)    


@app.route('/returns')
def returns():
   return render_template('returns.html')    


@app.route('/request')
def returnrequest():
   return render_template('return-request.html')    



@app.route('/login')
def login():
   return render_template('login.html')   


# @app.route('/registration')
# def registration():
#    return render_template('registration.html')  



if(__name__)=='__main__':
      app.secret_key = 'super secret key'
      app.config['SESSION_TYPE'] = 'filesystem'
      app.run(debug=True)

