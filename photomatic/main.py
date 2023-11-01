from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from chat import get_response 


import pymysql



app = Flask(__name__)



app.secret_key = 'your secret key'

conn=pymysql.connect(host="localhost",user="root",password="akshaycr97",db="login")

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
 msg = ''
 if request.method == 'POST':
  username = request.form['username']
  password = request.form['password']
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM account1 WHERE username = % s AND password = % s', (username, password, ))
  account=cursor.fetchone()
  cursor.close()
  
  msg='account not found'
  if account:
    data=account[2]
    if data=='admin':
      return render_template("admin.html")
    else:
      return render_template("index.html")
  else:
    return render_template('login.html', msg=msg)
 return render_template("login.html")
@app.route('/register',methods=['GET','POST'])
def register():
  msg=''
  if request.method=='POST' and 'username' in request.form and 'password' in request.form:
    username=request.form['username']
    password=request.form['password']
    type='user'
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM account1 WHERE username=%s',(username,))
    account=cursor.fetchone()
    if account:
      msg='already have an account'
    else:
      cursor.execute('INSERT INTO account1 VALUES(%s,%s,%s)',(username,password,type,))  
      cursor.connection.commit()
      msg='you have successfully registered'
      return render_template('login.html')
  return render_template('register.html')
  
@app.route('/about')
def about():
  return render_template('about.html')
@app.route('/profile')
def profile():
  return render_template('profile.html')
@app.route('/enquiry')
def enquiry():
  return render_template('enquiry.html')
@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        text=request.get_json().get("message")
        response =get_response(text)
        message ={"answer":response}
        return jsonify(message)
@app.route('/home')
def home():
  return render_template('index.html')
@app.route('/contact')
def contact():
  return render_template('contact.html')
@app.route('/adloginfo')
def adloginfo():
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM account1')
  data=cursor.fetchall()
  return  render_template('logindetails.html',data=data)
@app.route('/review' ,methods=['POST'])
def review():
  name=request.form['name']
  email=request.form['email']
  phonenumber=request.form['phone']
  message=request.form['message']
  cursor=conn.cursor()
  cursor.execute('INSERT INTO review VALUES(%s,%s,%s,%s)',(name,email,phonenumber,message,))  
  cursor.connection.commit()
  return render_template('index.html')
@app.route('/reviewinfo')
def reviewinfo():
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM review')
  data=cursor.fetchall()
  return  render_template('reviewdetails.html',data=data)
@app.route('/admissiondelete',methods=['POST'])
def admissiondelete():
  email=request.form['email']
  cursor = conn.cursor()
  cursor.execute('DELETE FROM admission WHERE email=(%s)',(email,))
  cursor.connection.commit()
  return redirect('admissioninfo')

@app.route('/logindelete',methods=['POST'])
def logindelete():
  password=request.form['password']
  cursor = conn.cursor()
  cursor.execute('DELETE FROM account1 WHERE password=(%s)',(password,))
  cursor.connection.commit()
  return redirect('adloginfo')

@app.route('/reveiwdelete',methods=['POST'])
def reviewdelete():
  email=request.form['email']
  cursor = conn.cursor()
  cursor.execute('DELETE FROM review WHERE email=(%s)',(email,))
  cursor.connection.commit()
  return redirect('reviewinfo')



@app.route('/admission')
def admission():
  return render_template('admission.html')
@app.route('/admissioninsert' ,methods=['POST'])
def admissioninsert():
  name=request.form['name']
  email=request.form['email']
  phonenumber=request.form['phone']
  department=request.form['department']
  accountnumber=request.form['accountnumber']
  accholdername=request.form['accholdername']
  drivelink=request.form['drivelink']
  cursor=conn.cursor()
  cursor.execute('INSERT INTO admission VALUES(%s,%s,%s,%s,%s,%s,%s)',(name,email,phonenumber,department,accountnumber,accholdername,drivelink))  
  cursor.connection.commit()
  return render_template('admission.html')
@app.route('/admissioninfo')
def admissioninfo():
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM admission')
  data=cursor.fetchall()
  return  render_template('admissiondetails.html',data=data)

@app.route('/tankyou')
def tankyou():
  return render_template('tankyou.html')
  
if __name__=="__main__":
    app.run(debug=True)
