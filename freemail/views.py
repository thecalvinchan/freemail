from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from pymongo import MongoClient
from django.core.mail import send_mail
client = MongoClient()
db = client.freemail_database

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

def generate_hash(email):
   return email


def confirmation(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        confs = db.confs
        new_conf = { "email" : email,
                     "date" : 
                     "hash"  : generate_hash(email + SALT)}
        confs.insert(new_conf)
    return HttpResponse('Confirmation page created')
        

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
