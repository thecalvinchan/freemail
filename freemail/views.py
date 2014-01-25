from django.http import HttpResponse
from pymongo import MongoClient
client = MongoClient()
db = client.freemail_database
gmails = db.gmails
new_gmail = { u'jeffreywang93' : u'ooJeffree@facebook.com'}

gmails_id = gmails.insert(new_gmail)

print(gmails_id)
print(gmails.find_one())

def index(request):
    return HttpResponse("Hello Werld")

def addUser(request, gmail, fb):
    return HttpResponse("Gmail is: " + gmail + ". Facebook is: " + fb)
