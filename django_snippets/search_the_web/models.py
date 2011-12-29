from google.appengine.ext import db

class User(db.Model):
    userip = db.StringProperty()
    uid = db.DateTimeProperty(auto_now_add=True) # spoof 'install date' for Alexa toolbar
