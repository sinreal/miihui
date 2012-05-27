#coding:utf-8
from datetime import datetime

from  config import options
from mongoengine import *

Model=Document
DB=options.get("DB")
connect(DB)

STATIC_FILE_URL=options.get("static_file_url")



class Auth_bind(Model):
    #user id
    ID=IntField(min_value=101,required=True,unique=True)
    #openid"sina+sinaid"
    opid= StringField(max_length=100)
    access_token =StringField(max_length=200)
    expires_in=StringField(max_length=200)
    #other info,maybe
    flag=StringField(max_length=200)

class  Tweet(Model):
       ID=IntField(min_value=1,required=True,unique=True)
       AutherID=IntField(required=True)
       SubjectID=IntField()
       content=StringField(max_length=1000,required=True)
       flag=IntField()  #flag some actions like share 1 means share,0 means dont show
       created = DateTimeField(default=datetime.now)



class Collect(Model):
     #修改为ID为商品ID
     #
     ID=IntField(required=True)
     #items=ListField(IntField())
     userlist=ListField(IntField())

class Notify(Model):
    #all requied
    sender=IntField(default=0) #0 is amdin
    receiver=IntField()
    content=StringField(max_length=400)
    label=StringField(max_length=200)
    link=StringField(max_length=400)
    type=StringField(max_length=20,default="reply")
    created=DateTimeField(default=datetime.now)
    #read or not?
    

    






