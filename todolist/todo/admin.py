from django.contrib import admin
from .models import *
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.admin import TokenAdmin

# # Register your models here.
# admin.site.unregister(Token)
# admin.site.register(Token)
admin.site.register(ToDo)
admin.site.register(Users)