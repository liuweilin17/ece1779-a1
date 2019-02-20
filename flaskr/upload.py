from flask import render_template, request, flash, redirect, url_for, session
from flaskr import app
from flaskr import db
from werkzeug.utils import secure_filename
import os
import hashlib
from flaskr.models import Image
from flaskr.openCV import face_detect_cv3
from flaskr.Pillow import thumbs
import traceback

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
        print("new image")
        # set the cursor to the beginning of the file
        file.seek(0)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # create thumbnail
        size = [200, 200]
        thumb = thumbs.Thumbs(size)
        thumb.run(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("create thumbnail of raw")

        # face detect
        ft = face_detect_cv3.FaceDetect()
        faceNum, output_img = ft.run(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("face detection")
        if output_img:
            thumb.run(output_img)
            print("create thumbnail of faces")

        # insert new image path
        image1 = Image(path=filename, userid=session['user']['userid'])
        db.session.add(image1)
        db.session.commit()
        print('insert new image path into database')

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
    try:
        valid, msg, file = checkImageRequest(request)
        print(msg)
        output_img = ''
        if valid:
            output_img = save_file(file)
        return output_img

    except Exception as e:
        # print(e)
        traceback.print_tb(e.__traceback__)
        return render_template('error.html', msg='something goes wrong~')
