from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    secret = models.CharField(max_length=20)

class Session(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=40, unique=True)
    expires_in = models.DateTimeField()
    scope = models.CharField(max_length=30, null=True)
    refresh_token = models.CharField(max_length=40, unique=True)

class Profile(models.Model):
    npm = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=50, default='')
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)