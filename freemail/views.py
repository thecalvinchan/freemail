from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from pymongo import MongoClient
from django.core.mail import send_mail
import datetime
import random
import string
import json
client = MongoClient()
db = client.freemail_database

ALPHABET = string.ascii_letters + string.digits

import settings

import os
SALT = os.environ.get('DJANGO_SALT')

import hashlib

def index(request):
    # return HttpResponse(settings.TEMPLATE_DIRS)
    return render(request, 'index.html')

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
              'contact@freemail.com',
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
        email = request.POST["email"]
        password = request.POST["password"]
        confs = db.confs
        new_conf = { "email" : email,
                     "date" : datetime.datetime.utcnow(),
                     "hash"  : generate_hash(password + generate_salt())}
        confs.insert(new_conf)
    return HttpResponse(json.dumps(new_conf), content_type="application/json")
        

def recieveEmailINTHEASS(request):
    request["from"] = US
    sendgrid[send-email](request)
    return HttpResponse("All Good")

def testPath(request, path):
    return HttpResponse(path)

def confirm(request, email, hashed):
    return redirect('/index.html?email=' + email + '&hash=' + hashed)
    # confs = db.confs
    # conf = confs.find_one({"email": email, "hash": hashed})
