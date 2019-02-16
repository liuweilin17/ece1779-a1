# access to the home page

from flask import render_template, url_for, session, redirect
from flaskr import app
from flaskr.models import Image

def getFaces(img):
    name, type = img.rsplit('.')
    return name + '_faces.' + type

def getThumbs(img):
    name, type = img.rsplit('.')
    return name + '_thumb.' + type

@app.route('/')
@app.route('/home')
def home():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        images = Image.query.filter_by(userid=user['userid'])
        images = [[image.imageid, getThumbs(image.path), image.path, getThumbs(getFaces(image.path)), getFaces(image.path)] for image in images]
        print(images)
        return render_template('home.html', images=images)