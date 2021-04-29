from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        exclude=[]

class ToDoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDo
        # fields = []
        exclude = []