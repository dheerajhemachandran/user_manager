from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint("auth", __name__)


@auth.route("/login",methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("successful login",category="success")
                login_user(user,remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("incorrect password",category="error")
        else:
            flash("user does'nt exist")            

    return render_template("login.html",user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up",methods=['POST','GET'])
def signup():
    email=request.form.get("email")
    name=request.form.get("firstName")
    pass1=request.form.get("password1")
    pass2=request.form.get("password2")

    user=User.query.filter_by(email=email).first()
    if user:
        flash("user already exist",category="error")    
    elif(email==None or name==None):
        pass
    elif(len(email)<2):
        flash("email must be greater than 2 characters",category="error")
    elif(len(name)<4):
        flash("name must be greater than 4 characters",category="error")
    elif(len(pass1)<=6):
        flash("password must be greater than 6 characters",category="error")
    elif(pass1!=pass2):
        flash("passwords don't match",category="error")
    else:
        new_user=User(email=email,first_name=name,password=generate_password_hash(pass1,method="sha256"))
        db.session.add(new_user)
        db.session.commit()
        flash("account created succesfully",category="success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html",user=current_user)