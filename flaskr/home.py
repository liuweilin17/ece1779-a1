from flask import render_template, url_for, session, redirect
from flaskr import app
from flaskr.models import Image
import traceback

def get_faces(img):
    name, type = img.rsplit('.')
    return name + '_faces.' + type

def get_thumbs(img):
    name, type = img.rsplit('.')
    return name + '_thumb.' + type

@app.route('/')
@app.route('/home')
def home():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        try:
            images = Image.query.filter_by(userid=user['userid'])
            images = [[image.imageid, get_thumbs(image.path), image.path,
                       get_thumbs(get_faces(image.path)), get_faces(image.path)] for image in images]
            return render_template('home.html', images=images)
        except Exception as e:
            # print(e)
            traceback.print_tb(e.__traceback__)
            return render_template('error.html', msg='something goes wrong~')
