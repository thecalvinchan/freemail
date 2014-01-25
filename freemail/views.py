from django.http import HttpResponse
from django.template.response import TemplateResponse
from pymongo import MongoClient
client = MongoClient()
db = client.freemail_database

import os
SALT = os.environ.get('DJANGO_SALT')

def index(request):
    t = TemplateResponse(request,'../public/index.html')
    t.render()
    return HttpResponse(t.content)

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
    
def sendConf(request, email):
    confs = db.confs
    new_conf = { "email" : email,
                 "hash"  : generate_hash(email + SALT)}
    confs.insert(new_conf)
    return HttpResponse('Confirmation page created')
