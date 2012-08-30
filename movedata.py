#!/usr/bin/python2.6
#coding:utf-8

#把tweet中的数据分离出来

from models.user import User
from models.models import *
from models.share_items import *



#for u in User.objects():
#    print u.username
"""
for  t in Tweet.objects():
      print t.flag
      if t.flag==1:
          share=Share_items(ID=Share_items.objects.count()+1,creatorID=t.AutherID,
          itemID=t.SubjectID,created=t.created)
          share.save()
          
"""

#new tweet
for  t in Tweet.objects().order_by("ID"):
    if t.flag==1:
          t.delete()
          
