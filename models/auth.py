#encoding:utf-8


#邮箱验证，密码绑定

from  config import options
from mongoengine import *
from datetime import datetime

Model=Document
DB=options.get("DB")
connect(DB)


#Class  Email_verify(Model):
       
