from mongoengine import connect
from models import Members, Requests
from datetime import datetime
import dns
from encrypt import encrypt_password, check_encrypted_password
import urllib


# connect('zpyl', host='mongomock://localhost', alias='default')
connect('zpyl6', host='localhost', port=27017, alias='default')
# connect(host='') # Live DB
def init_db():
    members = Members.objects.all()