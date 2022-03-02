from dataclasses import fields
from django.shortcuts import render
from todoapi import serializers
from todoapi.serializers import TodoSerializer,UserSerializer
from todoapi.models import User,Todo
import datetime

from django.http import HttpRequest, JsonResponse
from django.http import HttpResponse
from django.contrib.auth import hashers
import jwt,datetime
import json

PREFIX_JWT = 'Bearer '

def welcome(request):
    mywelcome = {
        "message":"Welcome to my APIs"
    }
    return JsonResponse(mywelcome)

def signup(request):
    
    # API 1: Sign up
    if request.method == 'POST':
        data = json.loads(request.body)
        data['password'] = hashers.make_password(data['password'])
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status":"200","message":"Signup successfully","data":serializer.data},status=201,safe=False)
        else:
            return JsonResponse({"status":"401","message":"Signup failed"})


def signin(request):
    # API 2: Sign in
    if request.method == 'POST':
        data = json.loads(request.body)

        if not data:
            return JsonResponse({"status":"400","message":"Username and password required"})
        
        user = User.objects.filter(username=data['username']).first()
        if user is None:
            return JsonResponse({"status":"400","message":"Username not found"})

        if hashers.check_password(data['password'],user.password):
            payload_jwt = {
                'username':data['username'],
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.now()
            }
            token = jwt.encode(payload_jwt,"todoapp",algorithm='HS256')
            return JsonResponse({"status":"200","message":"Signin successfully",'jwt_token':token},status=200,safe=False)

        return JsonResponse({"status":"400","message":"Password incorrect"})

def todo(request):
    try:
        header = request.headers
        token = header['Authorization'][7:]
        payload = jwt.decode(token, "todoapp", algorithms=["HS256"])
    except:
        return JsonResponse({'status':401,'message':'Failed authorized JWT token'},status=401)

    # API 6: Get all todos
    if request.method == 'GET':
        todolist = Todo.objects.all()
        serializer = TodoSerializer(todolist,many=True)
        return JsonResponse(serializer.data,safe=False) # Serializer is a non-dict object

    # API 3: Add todo
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(username=payload['username'])
        data['userid'] = payload['username']
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status':201,'message':'Add a todo successfully','data':serializer.data},status=201,safe=False)
        else:
            return JsonResponse({'status':400,'message':'Failed to add a todo'},status=400)

def todoid(request):

    try:
        header = request.headers
        token = header['Authorization'][7:]
        payload = jwt.decode(token, "todoapp", algorithms=["HS256"])
    except:
        return JsonResponse({'status':401,'message':'Failed authorized JWT token'},status=401)

    try:
        data = json.loads(request.body)
        id = data['id']
        todo = Todo.objects.get(id=id)
    except:
        return JsonResponse({'status':404,'message':'Object ID is not available'},status=400)

    # API 7: Get todo by ID
    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return JsonResponse({'status':201,'message':'Retrieve a todo successfully','data':serializer.data},status=201,safe=False)

    # API 4: Update todo
    if request.method == 'PATCH':
        data = json.loads(request.body)
        del data['id']
        serializer = TodoSerializer(todo)
        newtodo = TodoSerializer.update(self=serializer,instance=todo,validated_data=data)
        if serializer:
            newtodo.save()
            dataretrieve = TodoSerializer(newtodo)
            return JsonResponse({'status':201,'message':'Update a todo successfully','data':dataretrieve.data},status=201,safe=False)
        return JsonResponse({'status':400,'message':'Failed to update a todo'},status=400)

    # API 5: Remove todo
    if request.method == 'DELETE':
        todo.delete()
        return JsonResponse({'status':201,'message':'Removed todo'},status=201)

def getuser(request):

    try:
        header = request.headers
        token = header['Authorization'][7:]
        payload = jwt.decode(token, "todoapp", algorithms=["HS256"])
    except:
        return JsonResponse({'status':401,'message':'Failed authorized JWT token'},status=401)

    # API 8: Get all user
    if request.method == 'GET':
        userlist = list(User.objects.all().values('username'))
        return JsonResponse({'status':201,'message':'Retrieve all users','data':userlist},status=201,safe=False) # Serializer is a non-dict object

def assign(request):

    try:
        header = request.headers
        token = header['Authorization'][7:]
        payload = jwt.decode(token, "todoapp", algorithms=["HS256"])
    except:
        return JsonResponse({'status':401,'message':'Failed authorized JWT token'},status=401)

    try:
        data = json.loads(request.body)
        user = User.objects.get(username=data['username'])
        userassign = User.objects.get(username=payload['username'])
        todo = Todo.objects.get(id=data['todoid'])
    except:
        return JsonResponse({'status':404,'message':'Object ID or User is not available'},status=400)
        
    # API 9: Assign todo to a user
    if request.method == 'POST':

        if data['username']==payload['username']:
            return JsonResponse({'status':400,'message':'Cannot assign a task for yourself'},status=401)

        fields = {
            "userid":user,
            "assignedby":userassign,
        }
        serializer = TodoSerializer(todo)
        newdata = TodoSerializer.update(self=serializer,instance=todo,validated_data=fields)
        if newdata:
            newdata.save()
            dataretrieve = TodoSerializer(newdata)
            return JsonResponse({'status':201,'message':'Assign a todo successfully','data':dataretrieve.data},status=201,safe=False)
        return JsonResponse({'status':400,'message':'Failed to assign todo'},status=400)

def userall(request):

    try:
        header = request.headers
        token = header['Authorization'][7:]
        payload = jwt.decode(token, "todoapp", algorithms=["HS256"])
    except:
        return JsonResponse({'status':401,'message':'Failed authorized JWT token'},status=401)

    try:
        data = json.loads(request.body)
        user = User.objects.get(username=data['username'])
    except:
        return JsonResponse({'status':404,'message':'User is not available'},status=400)

    # API 10: Get all task by username
    if request.method == 'GET':
        todolist = Todo.objects.filter(userid=data['username']).all()
        list = TodoSerializer(todolist,many=True) # instance
        dataretrieve = TodoSerializer(list,many=True)
        if list:
            return JsonResponse({'status':201,'message':'Retrieving tasks successfully','data':list.data},status=201,safe=False)
        else:
            return JsonResponse({'status':400,'message':'Failed retrieving todos of a user'},status=400)

