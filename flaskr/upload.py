from flask import render_template, request, flash, redirect, url_for, session
from flaskr import app
from flaskr import db
from werkzeug.utils import secure_filename
import os
import hashlib
from flaskr.models import Image
from flaskr.openCV import face_detect_cv3
from flaskr.Pillow import thumbs

@app.route('/upload')
def upload():
    user = session['user'] if 'user' in session else None

    if not user:
        return redirect(url_for('login'))
    else:
        return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_file(file):
    output_img = ''
    filename = secure_filename(file.filename)
    filetype = filename.rsplit('.', 1)[1].lower()
    img_key = hashlib.md5(file.read()).hexdigest()
    filename = img_key + '.' + filetype
    userid=session['user']['userid']
    image = Image.query.filter_by(path=filename, userid=userid).first()

    if not image: # file not exists for userid
        # set the cursor to the beginning of the file
        file.seek(0)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # insert new image path
        image1 = Image(path=filename, userid=session['user']['userid'])
        db.session.add(image1)
        db.session.commit()

        # create thumbnail
        size = [200, 200]
        thumb = thumbs.Thumbs(size)
        thumb.run(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # face detect
        ft = face_detect_cv3.FaceDetect()
        faceNum, output_img = ft.run(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if output_img:
            thumb.run(output_img)

    return img_key + '_faces.' + filetype

def checkImageRequest(request):
    valid, msg, file = True, '', None
    if request.method == 'POST':
        if 'customFile' in request.files:
            file = request.files['customFile']
            if file.filename != '':
                if not file:
                    valid = False
                    msg = 'file is empty'
                elif not allowed_file(file.filename):
                    valid = False
                    msg = 'invalid file type'
                else:
                    valid = True
                    msg = 'success'
            else:
                valid = False
                msg = 'no selected file'
        else:
            valid = False
            msg = 'no file part'
    else:
        valid = False
        msg = 'invalid method'

    return [valid, msg, file]

@app.route('/uploadImage', methods=['GET', 'POST'])
def uploadImage():
    valid, msg, file = checkImageRequest(request)
    output_img = ''
    if valid:
        output_img = save_file(file)
    return output_img