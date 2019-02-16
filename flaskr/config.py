import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ece1779-a1-secretkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+pymysql://liuwl:liuwl@localhost/ece1779'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir + '/images'
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
