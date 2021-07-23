from config import dataBase
from flask_login import UserMixin

class userRecipes(dataBase.Model):
    __tablename__ = 'userRecipes'
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    recipe = dataBase.Column(dataBase.String, nullable=False)
    userImages_id = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('userImages.id'), nullable=False)
    userImages = dataBase.relationship('userImages', backref=dataBase.backref('recipes', lazy=True))

class userImages(dataBase.Model):
    __tablename__ = 'userImages'
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    userInfo_id = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('userInfo.id'), nullable=False)
    userInfo = dataBase.relationship('userInfo', backref=dataBase.backref('images', lazy=True))
    path = dataBase.Column(dataBase.String, unique=True, nullable=False)

class userInfo(dataBase.Model, UserMixin):
    __tablename__ = 'userInfo'
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    username = dataBase.Column(dataBase.String(20), nullable=False)
    email = dataBase.Column(dataBase.String(30), unique=True, nullable=False)
    password = dataBase.Column(dataBase.String(40), nullable=False)
    confirmed = dataBase.Column(dataBase.Boolean, nullable=False, default=False)
