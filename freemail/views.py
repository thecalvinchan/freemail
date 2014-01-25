from django.http import HttpResponse
from pymongo import MongoClient
client = MongoClient()
db = client.freemail_database

def index(request):
    return HttpResponse("Hello Werld")

def addUser(request, gmail, fb):
    emails = db.emails
    new_email = { "gmail" : gmail,
                  "facebook" : fb }
    emails.insert(new_email)
    return HttpResponse("Gmail is: " + gmail + ". Facebook is: " + fb)
