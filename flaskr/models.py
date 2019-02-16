from flaskr import db

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    salt = db.Column(db.String(64))

    def __repr__(self): # how to print User
        return '<User {}>'.format(self.username)

    def serialize(self):
        return {
            'userid': self.userid,
            'username': self.username,
        }

class Image(db.Model):
    imageid = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(140))
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))

    def __repr__(self):
        return '<Post {}>'.format(self.path)