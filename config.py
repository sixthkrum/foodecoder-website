from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__, template_folder = "default")
app.secret_key = "XXXXXXXXXXXXX"
app.config['SECURITY_PASSWORD_SALT'] = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#app.config['UPLOAD_FOLDER'] = '/home/user/semester-5/software-project-website/website/static/temp'
#app.config['STATIC_FOLDER'] = '/home/user/semester-5/software-project-website/website/static'
app.config['UPLOAD_FOLDER'] = '/home/user/apps/foodecoder/static/temp'
app.config['STATIC_FOLDER'] = '/home/user/apps/foodecoder/static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'XXXXXXXXXXXXXXXXXXXXXX'
app.config['MAIL_PASSWORD'] = 'XXXXXXX'
app.config['MAIL_DEFAULT_SENDER'] = 'XXXXXXXXXXXXXXXXXXX'

dataBase = SQLAlchemy(app)
mail = Mail(app)
loginManager = LoginManager(app)
loginManager.login_view = 'auth.login'
Session(app)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import main as main_blueprint
app.register_blueprint(main_blueprint)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

from models import userInfo
@loginManager.user_loader
def loadUser(userId):
    return userInfo.query.get(int(userId))

if __name__ == "__main__":
    app.run()
