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
import datetime
import random
import string
import json
import os
import hashlib

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
    
# def sendConf(request):
#     confs = db.confs
#     new_conf = { "email" : email,
#                  "hash"  : hashlib.sha1(email + SALT).hexdigest() }
#     confs.insert(new_conf)
#     send_mail('[FreeMail] Email Confirmation',
#               'Confirm your account by clicking on the following link: ' + '<a href="localhost:5000/confirm/' + email + '/' + new_conf["hash"] + '">Here</a>',
#               'test@freemail.bymail.in',
#               [email],
#               fail_silently=False)
#     return HttpResponse('Confirmation page created')

def generate_hash(input_str):
    return hashlib.sha1(input_str).hexdigest()

def generate_salt():
    chars = [random.choice(ALPHABET) for _ in xrange(16)]
    return "".join(chars)

def confirmation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        # email = request.POST.get('email', None)
        # password = request.POST.get('password', None)
        confs = db.confs
        new_conf = { "email" : email,
                     "date" : datetime.datetime.utcnow(),
                     "hash"  : generate_hash(password + generate_salt())
        }
        confs.insert(new_conf)
        send_mail('[FreeMail] Email Confirmation',
                  'Confirm your account by clicking on the following link: ' + 'http://localhost:5000/confirm/?email=' + email + '&id=' + new_conf["hash"],
                  'amanaamazing@gmail.com',
                  [email],
                  fail_silently=False)
        return HttpResponse(json.dumps({"email": email, "success": True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"email": email, "success": False}), content_type="application/json",status=500)

@csrf_exempt
def inbound(request):
    return HttpResponse('YAY')

def testPath(request, path):
    return HttpResponse(path)

def printTest(request):
    tests = db.tests
    test = tests.find_one()
    return HttpResponse(test)

def confirm(request, email, hashed):
    return redirect('/index.html?email=' + email + '&hash=' + hashed)
