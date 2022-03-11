from django.contrib import admin
from .models import Client, Session, Profile

# Register your models here.

admin.site.register(Client)
admin.site.register(Session)
admin.site.register(Profile)