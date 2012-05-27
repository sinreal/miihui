# -*- coding: utf-8-*-
from  config import options
from mongoengine import *
from datetime import datetime

Model=Document
DB=options.get("DB")
connect(DB)

STATIC_FILE_URL=options.get("static_file_url")

class User(Model):
    ID=IntField(min_value=101,required=True,unique=True) #note that ID=count+101
    username = StringField(max_length=100, unique=True,required=True)
    email = StringField(max_length=50)
    #微博登录是没有密码的 没有邮箱的
    password = StringField(max_length=100, required=True)
    avatar = StringField(max_length=400)
    avatar_big=StringField(max_length=400)
    #need to remove big
    website = StringField(max_length=400) #todo urlfield
    role = IntField(default=2)
    location=StringField(max_length=50)
    reputation = IntField(default=10)
    token = StringField(max_length=16)
    created = DateTimeField(default=datetime.now)
    last_login=DateTimeField(default=datetime.now)
    last_notify = DateTimeField(default=datetime.now)
    intro=StringField(max_length=300)
    followings_count=IntField(default=0)
    followed_count=IntField(default=0)
    tweet_count=IntField(default=0)
    post=ListField(IntField())
    nodes_follow=ListField(IntField())
    #people i follow   
    followings=ListField(IntField()) 
    #peole follow me
    #followeds=ListField(IntField())
    #todo location
    #todo notify_count

      
    def get_avatar(self):
       avatar=self.avatar
       if not avatar:avatar="default.png"
       if avatar[0]!='h':
          return  STATIC_FILE_URL+"/"+avatar
       else:
          return  avatar
       
    def get_big_avatar(self):
       avatar=self.avatar_big
       if not avatar:avatar="default.png"
       if avatar[0]!='h':
          return  STATIC_FILE_URL+"/"+avatar
       else:
          return  avatar

