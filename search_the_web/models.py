from django.db import models

class User(models.Model):
    userip = models.CharField(max_length=15)
    uid = models.DateTimeField(auto_now_add=True) # spoof 'install date' for Alexa toolbar
