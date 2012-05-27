# -*- coding: utf-8-*-
from mongoengine import *
from datetime import datetime
from config import options
Model=Document
DB=options.get("DB")
connect(DB)


class  Share_items(Model):
       ID=IntField(min_value=1,required=True,unique=True)
       creatorID=IntField(required=True)
       itemID=IntField()
       #content=StringField(max_length=100)
       flag=IntField()  #flag 备用,如果赋值则不显示或者推荐等
       created = DateTimeField(default=datetime.now)


