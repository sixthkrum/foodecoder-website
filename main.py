import os
from flask import Flask, flash, request, redirect, render_template, url_for, session, Blueprint
from flask_session import Session
from werkzeug.utils import secure_filename
import filetype
#import QueryRecipe_SingleQuery # Implementation of query to a deep learning model which generates recipes for a food image
#import singlequeryfooddetector # Implementation of query to a deep learning model which finds if an image is of food or not
from config import app, dataBase
from flask_login import login_required, current_user, logout_user
from models import userInfo, userImages, userRecipes
import time
import ast

main = Blueprint('main', __name__)

recipeModel = None
foodDetectionModel = None

'''
# Original, currently removed
def isFoodImage(stream):
    global foodDetectionModel

    if foodDetectionModel is None:
        foodDetectionModel = singlequeryfooddetector.loadModel()

    if singlequeryfooddetector.detectFoodImage(stream, foodDetectionModel) >= 0.85 and not str(filetype.guess(stream)).find('image') == -1:
        stream.seek(0)
        return 1

    stream.seek(0)
    return 0
'''

# Dummy implementation
def isFoodImage(stream):
    return 1;

@main.route('/')
def landing():
    if current_user.is_anonymous:
        return render_template('landing.html')
    else:
        return redirect(url_for('main.profile'))

@main.route('/', methods = ['POST'])
def uploadImage():
    if 'file' not in request.files:
        flash('No file sent in post request')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)

    if file and isFoodImage(file):
        imageFileName = secure_filename(file.filename)[:20]
        imageFileName = str(time.time()) + '-' + imageFileName
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], imageFileName)
        file.save(filePath)
        session['uploadedImageName'] = imageFileName

        '''
        # Original implementation
        global recipeModel
        if recipeModel is None:
            recipeModel = QueryRecipe_SingleQuery.loadModel()

        session['uploadedFileResults'] = QueryRecipe_SingleQuery.getImageRecipe(filePath, recipeModel[0], recipeModel[1], recipeModel[2])

        if 'error' in session['uploadedFileResults']:
            flash(session['uploadedFileResults']['error'])
            return redirect(request.url)

        else:
            return redirect(url_for('main.results'))
        '''

        # Dummy implementation
        session['uploadedFileResults'] = { 
            'title' : 'Dummy',
            'ingredients' : ['i1', 'i2'] ,
            'recipe' : ['s1', 's2']
        } 
            

        return redirect(url_for('main.results'))

    else:
        flash('Only food images are allowed')
        return redirect(request.url)

@main.route('/results')
def results():
    if 'uploadedImageName' in session:
        uploadedImageName = session['uploadedImageName']
        informationDictionary = session['uploadedFileResults']
        session.pop('uploadedImageName', None)
        session.pop('uploadedFileResults', None)

        showNavbar = False
        username = ''

        if not current_user.is_anonymous:
            showNavbar = True
            username = current_user.username

        return render_template('results.html', uploadedImageName=uploadedImageName, informationDictionary=informationDictionary, showNavbar=showNavbar, username=username)

    else:
        if request.args.get("previousResults"):
            return render_template('results.html', uploadedImageName=session['results'][request.args.get("imageId")]['path'], informationDictionary=session['results'][request.args.get("imageId")]['informationDictionary'], showNavbar=True, username=current_user.username, previousResults=True)

        else:
            return redirect(url_for('main.landing'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)

@main.route('/profile', methods=['POST'])
@login_required
def userUploads():
    if 'file' not in request.files:
        flash('No file sent in post request')
        return redirect(request.url)

    file = request.files['file']
    saveResults = False

    if request.form.get('resultCheckbox') == 'save':
        saveResults = True

    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)

    if file and isFoodImage(file):

        imageFileName = secure_filename(file.filename)[:20]

        imageFileName = str(time.time()) + '-' + imageFileName

        if saveResults:
            imageFileName = str(current_user.id) + '-' + imageFileName

        filePath = os.path.join(app.config['UPLOAD_FOLDER'], imageFileName)
        file.save(filePath)
        session['uploadedImageName'] = imageFileName

        '''
        # Original implementation
        global recipeModel
        
        if recipeModel is None:
            recipeModel = QueryRecipe_SingleQuery.loadModel()

        session['uploadedFileResults'] = QueryRecipe_SingleQuery.getImageRecipe(filePath, recipeModel[0], recipeModel[1], recipeModel[2])

        if 'error' in session['uploadedFileResults']:
            errorMessage = session['uploadedFileResults']['error']
            os.remove(filePath)
            session.pop('uploadedImageName', None)
            session.pop('uploadedFileResults', None)
            flash(errorMessage)
            return redirect(url_for('main.landing'))

        else:
            if saveResults:
                newImage = userImages()
                newImage.userInfo_id = current_user.id
                newImage.path = imageFileName
                dataBase.session.add(newImage)
                dataBase.session.flush()
                newRecipe = userRecipes(recipe=str(session['uploadedFileResults']), userImages_id=newImage.id)
                dataBase.session.add(newRecipe)
                dataBase.session.commit()

                if 'resultsCalculated' in session and session['resultsCalculated']:
                    session['results'][str(newImage.id)] =  {'title': session['uploadedFileResults']['title'], 'path': newImage.path, 'informationDictionary': session['uploadedFileResults']}

            return redirect(url_for('main.results'))
        '''
        # Dummy implementation
        session['uploadedFileResults'] = { 
            'title' : 'Dummy',
            'ingredients' : ['i1', 'i2'] ,
            'recipe' : ['s1', 's2']
        }
        
        if saveResults:
                newImage = userImages()
                newImage.userInfo_id = current_user.id
                newImage.path = imageFileName
                dataBase.session.add(newImage)
                dataBase.session.flush()
                newRecipe = userRecipes(recipe=str(session['uploadedFileResults']), userImages_id=newImage.id)
                dataBase.session.add(newRecipe)
                dataBase.session.commit()

                if 'resultsCalculated' in session and session['resultsCalculated']:
                    session['results'][str(newImage.id)] =  {'title': session['uploadedFileResults']['title'], 'path': newImage.path, 'informationDictionary': session['uploadedFileResults']}

        return redirect(url_for('main.results'))

    else:
        flash('Only food images are allowed')
        return redirect(request.url)

@main.route('/previous-results')
@login_required
def previousResults():
    if 'resultsCalculated' in session and session['resultsCalculated']:
        if session['results']:
            return render_template('previous-results.html', username=current_user.username, savedResults=session['results'])

        else:
            flash("No results to show")
            return redirect(url_for('main.profile'))

    else:
        images = userImages.query.filter_by(userInfo_id=current_user.id).all()
        results = {}
        for image in images:
            recipeObject = userRecipes.query.filter_by(userImages_id=image.id).first()
            parsedRecipe = ast.literal_eval(recipeObject.recipe)
            results[str(image.id)] = {'title': parsedRecipe['title'], 'path': image.path, 'informationDictionary': parsedRecipe}

        if results:
            session['results'] = results
            session['resultsCalculated'] = True
            return render_template('previous-results.html', username=current_user.username, savedResults=results)

        else:
            flash("No results to show")
            return redirect(url_for('main.profile'))

@main.route('/previous-results', methods=['POST'])
@login_required
def deleteResults():
    imageId = request.form.get("imageId")

    if imageId in session['results']:
        del session['results'][imageId]

        imageQuery = userImages.query.filter_by(id=int(imageId))
        image = imageQuery.first()

        if image:
            imageQuery.delete()

            filePath = os.path.join(app.config['UPLOAD_FOLDER'], image.path)
            if os.path.exists(filePath):
                os.remove(filePath)

            userRecipes.query.filter_by(userImages_id=imageId).delete()

            dataBase.session.commit()

        if session['results']:
            return render_template('previous-results.html', username=current_user.username, savedResults=session['results'])

        else:
            flash("All results deleted, none to show")
            return redirect(url_for('main.profile'))


    else:
        return render_template('previous-results.html', username=current_user.username, savedResults=session['results'])
