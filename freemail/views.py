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
import sendgrid

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
    else:
        return HttpResponse(json.dumps({"email": email, "success": False}), content_type="application/json",status=500)

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
        

@csrf_exempt
def inbound(request):
<<<<<<< HEAD
    if request.method == 'POST':
        print(request.POST)
        data = request.POST.copy()
        from_email = data["from"]
        subject = data["subject"]
        data["subject"] = "from: [" + from_email + "] subject: [" + subject + "]"
        print(from_email)
        print(subject)

        #s = sendgrid.Sendgrid('Juwang', os.environ.get('DJANGO_SALT'), secure=True)
        #message = sendgrid.Message("jeffreywang93@gmail.com", subject, data["text"], "<p>HTML</p>")
        #print(message)
        #message.add_to("robin@sendgrid.com")
        #print(message)
        #s.smtp.send(message)
        send_mail(data["subject"], data["text"], data["from"], ["Aman Agarwal <amanaamazing@gmail.com>"], fail_silently=False)
    return HttpResponse('')
=======
    return HttpResponse('YAY')
>>>>>>> this is wrong but ill fix at merge


def testPath(request, path):
    return HttpResponse(path)

def printTest(request):
    tests = db.tests
    test = tests.find_one()
    return HttpResponse(test)
<<<<<<< HEAD

def confirm(request, email, hashed):
    return redirect('/index.html?email=' + email + '&hash=' + hashed)
=======
<<<<<<< HEAD
=======

def confirm(request, email, hashed):
    return redirect('/index.html?email=' + email + '&hash=' + hashed)
>>>>>>> this is wrong but ill fix at merge
>>>>>>> this is wrong but ill fix at merge
