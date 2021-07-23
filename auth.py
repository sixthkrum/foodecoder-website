from flask import Flask, flash, request, redirect, render_template, url_for, session, Blueprint
from config import dataBase, app
from confirmation import generateConfirmationToken, confirmToken, sendEmail
from werkzeug.security import generate_password_hash, check_password_hash
from models import userInfo, userImages, userRecipes
from flask_login import login_user, login_required, current_user, logout_user
import os

auth = Blueprint('auth', __name__)

@auth.route('/register')
def register():
    if current_user.is_anonymous:
        return render_template('register.html')
    else:
        return redirect(url_for('main.profile'))

@auth.route('/register', methods=['POST'])
def checkRegistration():
    if current_user.is_anonymous:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = userInfo.query.filter_by(email=email).first()

        if user:
            flash("User with this email already exists, please try another email")
            return redirect(url_for('auth.register'))

        newUser = userInfo(username = username, email = email, password = generate_password_hash(password, method = 'sha256'))
        dataBase.session.add(newUser)
        dataBase.session.commit()
        token = generateConfirmationToken(email)

        confirmationUrl = url_for('auth.confirmEmail', token=token, _external=True)
        html = render_template('mail-template.html', confirmationUrl=confirmationUrl)
        subject = "Please confirm your email"
        sendEmail(email, subject, html)

        flash("Registration complete, click on the confirmation link sent to your email to be able to login. Please check the spam folder if you do not see an email")
        return redirect(url_for('auth.login'))

    else:
        return redirect(url_for('main.profile'))

@auth.route('/confirm-registration/<token>')
def confirmEmail(token):
    try:
        email = confirmToken(token)
    except:
        flash("Invalid confirmation link")
        return redirect(url_for('auth.login'))

    user = userInfo.query.filter_by(email=email).first()

    if user.confirmed:
        flash("User has already been confirmed, proceed to login")
        return redirect(url_for('auth.login'))

    user.confirmed = True
    dataBase.session.add(user)
    dataBase.session.commit()
    flash("User confirmed! You can now login")
    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    if current_user.is_anonymous:
        return render_template('login.html')
    else:
        return redirect(url_for('main.profile'))

@auth.route('/login', methods=['POST'])
def checkLogin():
    if current_user.is_anonymous:
        email = request.form.get('email')
        password = request.form.get('password')
        user = userInfo.query.filter_by(email=email).first()

        if user and user.confirmed == True:
            if check_password_hash(user.password, password):
                session.clear()
                login_user(user, remember=True)
                return redirect(url_for('main.profile'))

            else:
                flash("Please check details and try again")
                return redirect(url_for('auth.login'))

        elif user and user.confirmed == False:
            flash("Please confirm account via link sent on email, check for email in spam folder too")
            return redirect(url_for('auth.login'))

        flash("Please check details and try again")
        return redirect(url_for('auth.login'))

    else:
        return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('main.landing'))

@auth.route('/delete-account')
@login_required
def deleteAccount():
    return render_template('delete-account.html', username=current_user.username)

@auth.route('/delete-account', methods=['POST'])
@login_required
def confirmDeletion():
    password = request.form.get('password')
    if not check_password_hash(current_user.password, password):
        flash("Incorrect Password Entered")
        return redirect(url_for('auth.deleteAccount'))

    else:
        userInfo.query.filter_by(id=current_user.id).delete()
        imageQuery = userImages.query.filter_by(userInfo_id=current_user.id)
        images = imageQuery.all()
        imageQuery.delete()

        for image in images:
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], image.path)
            if os.path.exists(filePath):
                os.remove(filePath)

        imageIds = [image.id for image in images]

        recipes = userRecipes.query.filter(userRecipes.userImages_id.in_(imageIds)).delete(synchronize_session='fetch')

        dataBase.session.commit()

        logout_user()

        flash("Your account has been successfully deleted")
        return redirect(url_for('main.landing'))
