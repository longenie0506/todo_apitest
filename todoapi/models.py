from email.policy import default
from typing import Set
from django.db import models
from enum import unique
from django.db import models
import uuid

# todo: id,name,description,userid,assignedby,dateofcompletion,status,dateofcreation,dateofmodification
# user: id,username,password
# Note: todo-assignedby is an external custom property to make task-assigning, value is another userid

class Todo(models.Model):
    option_status = [(False,'NEW'),(True,'COMPLETE')]
    id = models.AutoField(primary_key=True,editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    userid = models.ForeignKey('User',blank=False,null=False,on_delete=models.CASCADE,related_name="owner")
    assignedby = models.ForeignKey('User',blank=True,null=True,default=None,on_delete=models.SET(None),related_name="created_by") # assigned by "None" means the user created todo for himself
    dateofcompletion = models.CharField(max_length=100)
    status = models.CharField(default='NEW', max_length=20)
    dateofcreation = models.DateTimeField(auto_now_add=True)
    dateofmodification = models.DateTimeField(auto_now=True)

class User(models.Model):
    username = models.CharField(max_length=48,unique=True,primary_key=True)
    password = models.TextField(null=False,blank=False)

