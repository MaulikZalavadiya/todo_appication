from django.shortcuts import render
from rest_framework.permissions import BasePermission, IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.generics import GenericAPIView
from .models import *
from .serializers import *
from datetime import date, datetime, timedelta
from rest_framework.response import Response
from http.client import responses as HTTPStatus
import random
from django.core.mail import send_mail
from django.conf import settings
from .serializers import *


def APIResponse(data=None, notification=None, *args, **kwargs):
    response = {
        'notification': {}
    }
    if (notification is not None) and len(notification) == 2:
        response['notification'] = {
            'type': notification[0],
            'message': notification[1]
        }
        response['data'] = data
    resp = Response(response, *args, **kwargs)
    resp.data['status'] = resp.status_code
    resp.data['status_type'] = HTTPStatus[resp.status_code]
    return resp
# Create your views here.


class SignUpView(CreateModelMixin, 
               GenericAPIView):
    permission_classes = [AllowAny]

    def generete_password():
        return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
    
    def post(self, request, *args, **kwargs):
        if Users.objects.filter(email=request.data.get('email')).exists():
            password=generete_password()
            create = Users.objects.create(email=request.data.get('email'), password=password)
            send_mail('sent password',
                          f'Hi,\n Your password is ' + password,
                          settings.EMAIL_HOST_USER,
                          [request.data.get('email'), ])
            return APIResponse(notification=('success', 'user is singup'), status=200)
        return APIResponse(notification=('error', 'somthing wrong'), status=400)



class LoginView(CreateModelMixin, 
               GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if Users.objects.filter(email=request.data.get('email'), password=request.data.get('password')).exists():
            token, created = Token.objects.get_or_create(
                        user=request.user)
            return APIResponse(notification=('success', 'user is singup'), status=200)
        return APIResponse(notification=('error', 'somthing wrong'), status=400)



class ToDoView(ListModelMixin,
                RetrieveModelMixin, 
                UpdateModelMixin, 
                CreateModelMixin, 
                DestroyModelMixin,
                GenericAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = [IsAuthenticated]

    def searchfilter(self, request, queryset):
        # if 'search' in self.request.GET:
        fields = [f for f in ToDo._meta.fields if isinstance(f, (CharField))]
        queries = [Q(**{f.name + "__contains": self.request.GET.get('search')}) for f in fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        return queryset.filter(qs)

    def list(self, request, *args, **kwargs):
        queryset = seld.queryset()
        if 'search' in self.request.GET:
            queryset = self.searchfilter(request,queryset)
        serializer = ToDoSerializer(queryset, many=True)
        return APIResponse(data=serializer.data, notification=('success', 'todo list'), status=200)

    def create(self, request, *args, **kwargs):
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(notification=('success', 'todo saved'),
                               status=200)
        else:
            return APIResponse(data=serializer.errors, notification=('errors', 'somthing wrong'),
                               status=400)

    def update(self, request, *args, **kwargs):
        serializer = ToDoSerializer(self.queryset().get(pk=kwargs['pk']), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(notification=('success', 'todo updated'),
                               status=200)
        else:
            return APIResponse(data=serializer.errors, notification=('errors', 'something wrong'), status=400)

    def destroy(self, request, *args, **kwargs):
        queryset = self.queryset().filter(pk=kwargs['pk']).first()
        queryset.delete()
        return APIResponse(notification=('success', 'todo deleted'), status=200)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

