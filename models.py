from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField,
    ListField, ReferenceField, StringField,
    ObjectIdField, IntField, BooleanField, FloatField
)

class Members(Document):
    meta = {'collection': 'members'}
    national_id_number = StringField(required=True)
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    phonenumber = StringField(required=True)
    home_address = StringField(required=True)
    province = StringField(required=True)
    district = StringField(required=True)
    polling_station = StringField(required=True)
    branch = StringField(required=True)
    youth_league = StringField(required=True)
    profile_image = StringField(required=True)
    date_of_registration = StringField(required=True)

class Requests(Document):
    meta = {'collection': 'requests'}
    phonenumber = StringField(required=True)
    main_root = StringField(required=True)
    root_option = StringField(required=True)
    user_response = StringField(required=True)
    date_of_request = StringField(required=True)
