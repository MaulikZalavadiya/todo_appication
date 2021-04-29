from django.db import models

TODO_STATUS = (
    ("PENDING", "PENDING"),
    ("COMPLETED", "COMPLETED")
)

# Create your models here.
class ToDo(models.Model):
    title = models.CharField(max_length=1000, null=True, blank=True)
    duedate = models.DateField(auto_now=True)
    category = models.CharField(max_length=20, choices=TODO_STATUS,default='PENDING')
    description = models.CharField(max_length=1000, null=True, blank=True)

class Users(models.Model):
    email = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=20, null=False, blank=False)