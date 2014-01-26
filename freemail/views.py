from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect, render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from pymongo import MongoClient
from django.core.mail import send_mail
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
    confs = db.confs
    new_conf = { "email" : email,
                 "hash"  : hashlib.sha1(email + SALT).hexdigest() }
    confs.insert(new_conf)
    send_mail('[FreeMail] Email Confirmation',
              'Confirm your account by clicking on the following link: ' + '<a href="localhost:5000/confirm/' + email + '/' + new_conf["hash"] + '">Here</a>',
              'amanaamazing@gmail.com',
              [email],
              fail_silently=False)
    return HttpResponse('Confirmation page created')

def generate_hash(input_str):
    return hashlib.sha1(input_str).hexdigest()

def generate_salt():
    chars = [random.choice(ALPHABET) for _ in xrange(16)]
    return "".join(chars)


def confirmation(request):
    if request.method == 'POST':
        post = request.POST
        post = post.copy()
        email = post.get('email')
	password = post.get('password')
        # email = request.POST.get('email', None)
        # password = request.POST.get('password', None)
        confs = db.confs
        new_conf = { "email" : email,
                     "date" : datetime.datetime.utcnow(),
                     #"hash"  : generate_hash(password + generate_salt())
	}
        confs.insert(new_conf)
        return HttpResponse(json.dumps(post), content_type="application/json")
    return HttpResponse("WHAT NOT POST?!?!?")

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
    # confs = db.confs
    # conf = confs.find_one({"email": email, "hash": hashed})

