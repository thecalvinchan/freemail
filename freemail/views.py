from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect, render_to_response
from django.core.context_processors import csrf
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import *
# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.views.decorators.csrf import csrf_response_exempt
from pymongo import MongoClient
from django.core.mail import send_mail
from bson.objectid import ObjectId
import datetime
import random
import string
import json
import os
import hashlib
import re

SALT = os.environ.get('DJANGO_SALT')
MONGO_URI = os.environ.get('MONGO_URI') 
client = MongoClient(MONGO_URI)
db = client.freemail_database

ALPHABET = string.ascii_letters + string.digits

@ensure_csrf_cookie
def index(request):
    # return HttpResponse(settings.TEMPLATE_DIRS)
    c = {}
    c.update(csrf(request))
    return render(request,'index.html',c)

# def addUser(request, gmail, fb):
#     emails = db.emails
#     new_email = { "gmail" : gmail,
#                   "facebook" : fb }
#     return HttpResponse("Gmail is: " + gmail + ". Facebook is: " + fb)

# def getAllUsers(request):
#     all_emails = ["facebook: '" + email[u'facebook'] + "' and gmail: '" + email[u'gmail'] + "'"
#         for email in db.emails.find()]
#     return HttpResponse('\n\n'.join(all_emails))
    
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
    elif request.method == 'GET':
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
        
def isFbEmail(email):
    result = re.match(r'^\w+@facebook.com', email)
    if result:
        return True
    else:
        return False

def get_from_email_from_subject(subject):
    result = re.match(r'^.*?from: \[(.*?)\].*?$', subject)
    return result.group(1)

@csrf_exempt
def inbound(request):
    if request.method == 'POST':
        data = request.POST.copy()
        email_data =  {}
        in_db = False
        users = db.users
        if isFbEmail(data["from"]):
            email_data["to"] = get_from_email_from_subject(data["subject"])
            user = users.find_one({"facebook" : data["from"]})
            if user:
                in_db = True
                email_data["from"] = user["email"]
            email_data["subject"] = data["subject"]
            email_data["text"] = data["text"]
        else:
            user = users.find_one({"email" : data["from"]})
            if user:
                in_db = True
                email_data["to"] = user["facebook"]
            email_data["from"] = "test@freemail.bymail.in"
            email_data["subject"] = "id: [" + generate_salt() + "], from: [" + data["from"] + "], subject: " + data["subject"]
            email_data["text"] = data["text"]

        if in_db:
            send_mail(email_data["subject"], email_data["text"], email_data["from"], [email_data["to"]], fail_silently=False)

        # users = db.users
        # to_addr = users.find_one({"email": from_email})['fb']
        

        #s = sendgrid.Sendgrid('Juwang', os.environ.get('DJANGO_SALT'), secure=True)
        #message = sendgrid.Message("jeffreywang93@gmail.com", subject, data["text"], "<p>HTML</p>")
        #print(message)
        #message.add_to("robin@sendgrid.com")
        #print(message)
        #s.smtp.send(message)
        return HttpResponse('INBOUND POST')
    return HttpResponse('INBOUND GET')

def testPath(request, path):
    return HttpResponse(path)

def printTest(request):
    tests = db.tests
    test = tests.find_one()
    return HttpResponse(test)

def confirm(request, email, hashed):
    return redirect('/index.html?email=' + email + '&hash=' + hashed)
