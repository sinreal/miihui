#coding:utf-8
from  config import options
from datetime import datetime

from mongoengine import *
Model=Document
DB=options.get("DB")
connect(DB)


#任务，暂时使用MB自己的代替
#主要任务  验证邮件 同步微博


class Task(Model):
   created = DateTimeField(default=datetime.now)
   jobtype=IntField() #1 sendmail # 2sysn weibo
   jobdetail=StringField(max_length=100,required=True)
   result=IntField(default=0)   # 0 a new job 1 job done ok ,-1 erro -2 erros
