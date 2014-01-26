from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect, render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from pymongo import MongoClient
from django.core.mail import send_mail
from bson.objectid import ObjectId
import datetime
import random
import string
import json

import os
SALT = os.environ.get('DJANGO_SALT')
MONGO_URI = os.environ.get('MONGO_URI') 
client = MongoClient(MONGO_URI)
db = client.freemail_database

ALPHABET = string.ascii_letters + string.digits

import settings
EMAIL_HOST = settings.EMAIL_HOST
EMAIL_HOST_USER = settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_USE_TLS = settings.EMAIL_USE_TLS


import hashlib

@ensure_csrf_cookie
def index(request):
    # return HttpResponse(settings.TEMPLATE_DIRS)
    c = {}
    c.update(csrf(request))
    return render(request,'index.html',c)

def addUser(request, gmail, fb):
    emails = db.emails
    new_email = { "gmail" : gmail,
                  "facebook" : fb }
    emails.insert(new_email)
    return HttpResponse("Gmail is: " + gmail + ". Facebook is: " + fb)

def getAllUsers(request):
    all_emails = ["facebook: '" + email[u'facebook'] + "' and gmail: '" + email[u'gmail'] + "'"
        for email in db.emails.find()]
    return HttpResponse('\n\n'.join(all_emails))
    
def sendConf(request):
    users = db.users
    new_conf = { "email" : email,
                 "hash"  : hashlib.sha1(email + SALT).hexdigest() }
    users.insert(new_conf)
    send_mail('[FreeMail] Email Confirmation',
              'Confirm your account by clicking on the following link: ' + '<a href="localhost:5000/confirm/' + email + '/' + new_conf["hash"] + '">Here</a>',
              'test@freemail.bymail.in',
              [email],
              fail_silently=False)
    return HttpResponse('Confirmation page created')

def generate_hash(input_str):
    return hashlib.sha1(input_str).hexdigest()

def generate_salt():
    chars = [random.choice(ALPHABET) for _ in xrange(16)]
    return "".join(chars)

@ensure_csrf_cookie
def user(request):
    #update user info
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data['user_id']
        session = data['session']
        fbemail = data['fbemail']
        print(fbemail)
        cur_session = db.sessions.find_one({"user_id": ObjectId(user_id)})
        try:
            print(cur_session)
            if cur_session["hash"] != session:
                return HttpResponse(json.dumps({"error":"Session is out of date"}), content_type="application/json",status=500)
        except:
            #user is not authenticated
            return HttpResponse(json.dumps({"error":"User Session could not be found"}), content_type="application/json",status=500)
        try:
            db.users.update({ "_id" : ObjectId(user_id) } , { "$set" : { "facebook" : fbemail} } , False)
        except:
            #user cannot be found
            return HttpResponse(json.dumps({"error":"An error occured."}), content_type="application/json",status=500)
        return HttpResponse(json.dumps({"success": True}), content_type="application/json")
    
@ensure_csrf_cookie
def confirmation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        salt = generate_salt()
        # email = request.POST.get('email', None)
        # password = request.POST.get('password', None)
        users = db.users
        new_conf = {
            "email" : email,
            "facebook" : None,
            "date" : datetime.datetime.utcnow(),
            "confhash"  : generate_hash(email + salt),
            "password" : generate_hash(password + salt),
            "salt" : salt,
            "confirmed" : False
        }
        users.insert(new_conf)
        send_mail('[FreeMail] Email Confirmation',
                  'Confirm your account by clicking on the following link: ' + 'http://localhost:5000/confirmation?email=' + email + '&id=' + new_conf["confhash"],
                  'amanaamazing@gmail.com',
                  [email],
                  fail_silently=False)
        return HttpResponse(json.dumps({"email": email, "success": True}), content_type="application/json")
        return HttpResponse(json.dumps({"email": email, "success": False}), content_type="application/json",status=500)
    if request.method == 'GET':
        data = request.GET
        email = data.get('email')
        hash = data.get('id')
        users = db.users
        try:
            user = users.find_one({"email" : email})
        except:
            #user does not exist
            return HttpResponse(json.dumps({"error":"User does not exist"}), content_type="application/json",status=500)
        if user["confhash"] != hash:
            #error
            return HttpResponse(json.dumps({"error":"Invalid authentication"}), content_type="application/json",status=500)
        user["confirmed"] = True
        users.save(user)
        c = {}
        c.update(csrf(request))
        return render(request,'index.html',c)

def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        users = db.users
        sessions = db.sessions
        try:
            user = users.find_one({"email" : email})
        except:
            #user does not exist
            return HttpResponse(json.dumps({"error":"Username is incorrect"}), content_type="application/json",status=500)
        hashedpassword = generate_hash(password + user["salt"])
        if hashedpassword != user["password"]:
            return HttpResponse(json.dumps({"error":"Password is incorrect"}), content_type="application/json",status=500)
        if user["facebook"] == None:
            action="facebook"
        else:
            action="overview"
        session = generate_hash(user["email"]+generate_salt())
        sessions.update({ "user_id" : user["_id"] } , { "$set" : { "hash" : session } } ,True)
        return HttpResponse(json.dumps({"action":action,"user_id":str(user["_id"]),"session":session}), content_type="application/json")
        

def recieveEmailINTHEASS(request):
    request["from"] = US
    sendgrid[send-email](request)
    return HttpResponse("All Good")

def testPath(request, path):
    return HttpResponse(path)

def inbound(request):
    tests = db.tests
    new_test = { "data" : request }
    tests.insert(new_test)
    print(tests)
    return HttpResponse('')

def printTest(request):
    tests = db.tests
    test = tests.find_one()
    return HttpResponse(test)

def confirm(request, email, hashed):
    return redirect('/index.html?email=' + email + '&hash=' + hashed)
    # users = db.users
    # conf = users.find_one({"email": email, "hash": hashed})

