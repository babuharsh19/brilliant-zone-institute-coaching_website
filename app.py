from flask import Flask, render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required,current_user,LoginManager,UserMixin
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = u"Please login to access this page"
login_manager.login_message_category = "info"
login_manager.login_view = 'login'

active = 'active'
local_server =False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/brilliant_zone'
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = parameter['prod_uri
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)
class Contact(db.Model):

    sno = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(300), nullable=False)

class Users(db.Model,UserMixin):
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

class Admin(db.Model,UserMixin):
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

class Courses(db.Model,UserMixin):
    
    sno = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    subheading = db.Column(db.String(50), nullable=False)
    form = db.Column(db.String(50), nullable=False)
    startdate = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(300), nullable=False)

@login_manager.user_loader  
def load_user(user_id): 
    return Users.query.get(int(user_id))

@app.route("/",methods = ['GET','POST'])
def home():
    return render_template("home.html",active=active)

@app.route("/register",methods = ['GET','POST'])
def register():
    if request.method == ['GET','POST']:
        
        name = request.form.get('signupName')
        email = request.form.get('signupEmail')
        phone = request.form.get('signupPhone')
        password = request.form.get('signupPassword')
        user = Users.query.filter_by(phone=phone).first()
        if user:
            flash('phone/Email address already exists')
            # return redirect(url_for('home'))
        else:
            entry = Users(name=name, email=email, phone=phone,password=password)
            db.session.add(entry)
            db.session.commit()
            flash('Registered successfully!')
            # return redirect(url_for('home'))
    return render_template("index.html")

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method == ['GET','POST']:
        phone = request.form.get('loginPhone')
        name = request.form.get('loginName')
        password = request.form.get('loginPassword')
        user = Users.query.filter_by(phone=phone).first()
        if not user or not password==user.password:
            flash("Either you are not registered or your password is incorrect")
            return redirect(url_for('home'))
        else:
            login_user(user)
            flash("Loggedin succesfully")
            return redirect(url_for('home'))
    return render_template('index.html')

@app.route("/logout",methods = ['GET','POST'])
# @login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/about",methods = ['GET','POST'])
def about():
    return render_template("about.html",active=active)

@app.route("/courses",methods = ['GET','POST'])
#@login_required
def courses():
    # courses = Courses.query.filter_by().all()[0:50]
    return render_template("courses.html",active=active)

@app.route("/contact",methods = ['GET','POST'])
def contact():
    if(request.method ==  'POST'):
    
        '''add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('mail')
        subject = request.form.get('subject')
        message = request.form.get('message')

        '''upload sno, name, email, subject, messageon database'''
        entry = Contact(name=name, email=email, subject=subject,message=message)
        db.session.add(entry)
        db.session.commit()
    return render_template("contact.html",active=active)

@app.route("/refer",methods = ['GET','POST'])
# @login_required
def refer():
    return render_template("refer.html",active=active)

@app.route("/notice",methods = ['GET','POST'])
# @login_required
def notice():
    return render_template("notice.html",active=active)

@app.route("/jnvenglish",methods = ['GET','POST'])
# @login_required
def jnvenglish():
    return render_template("jnvenglish.html",active=active)

@app.route("/programmingjobready",methods = ['GET','POST'])
# @login_required
def programmingjobready():
    return render_template("programmingjobready.html",active=active)

@app.route("/jnvhindi",methods = ['GET','POST'])
# @login_required
def jnvhindi():
    return render_template("jnvhindi.html",active=active)

@app.route("/dsa",methods = ['GET','POST'])
# @login_required
def dsa():
    return render_template("dsa.html",active=active)

@app.route("/cpythoncpp",methods = ['GET','POST'])
# @login_required
def cpythoncpp():
    return render_template("cpythoncpp.html",active=active)

@app.route("/webdev",methods = ['GET','POST'])
# @login_required
def webdev():
    return render_template("webdev.html",active=active)

@app.route("/add", methods=['GET','POST'] )
# @login_required
def addcourse():
    if(request.method ==  'POST'):
      title = request.form.get('title')
      subheading = request.form.get('subheading')
      form = request.form.get('form')
      content = request.form.get('content')
      startdate = request.form.get('startdate') 
      entry = Courses(title=title,subheading=subheading,form=form,content=content,startdate=startdate)
      db.session.add(entry)
      db.session.commit()
      return redirect(url_for('/home'))  
    return render_template('addcourse.html')

@app.route("/delete/<sno>" , methods=['GET', 'POST'])
@login_required
def delete(sno):
    if current_user.email==Admin.query.get('email'):
        course = Courses.query.filter_by(sno=sno).first()
        db.session.delete(course)
        db.session.commit()
    return redirect(url_for('/home'))

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
# app.run(debug=True)