#coding:utf-8

import web

from models.user import User
from models.models import *
from models.node import Node 
from lib.kit import Auth
from lib.time_format import friendly_time
from lib.decorators import authenticate	
from lib.common import render



class People:
 # @authenticate	
  def GET(self,uid):
      myuid=Auth.uid()
      page=int(web.input().get("page","1")) 
      thisguy=User.objects(ID=int(uid)).first()
      if not thisguy:
          return  render.notfound()
      thisguy.tweet_count=Tweet.objects(AutherID=thisguy.ID).count()
      counts = thisguy.followings_count,thisguy.followed_count,thisguy.tweet_count
      
      #update count
      if page*20<counts[2]:
         next=page+1
      elif page*20-counts[2]>20 :
         return  web.notfound()
      else:  
         next=None

      if Auth.is_login():
          me=User.objects(id=Auth.uid()).first()
      else:
          me=None
          
      if not me:
           relation=None
      elif me==thisguy:
          relation="self"
      elif thisguy.ID in me.followings:
           relation="ifollowhim"
      else:
           relation=None
      # do i follow that people?
      datalist=[]
      posts=Tweet.objects(AutherID=thisguy.ID).order_by("-ID")[(page-1)*20:page*20]
  
      for p in posts:
          if p.SubjectID>0:
              if p.flag==1:
                 datalist.append(("share" ,Node.objects(ID=p.SubjectID).first(),p, friendly_time(p.created).decode("utf-8")))
              elif p.flag==-1:
                  pass   
              else:   
                 datalist.append(("comment" ,Node.objects(ID=p.SubjectID).first(),p, friendly_time(p.created).decode("utf-8")))
          elif p.flag==-1:
                  pass
          else: 
                datalist.append(("say",p,friendly_time(p.created).decode("utf-8")))  
      return  render.user(user=me,thisguy=thisguy,counts=counts,next=next,datalist=datalist,relation=relation)


class Follow:
  @authenticate              
  def POST(self):
    myuid=Auth.uid()
    foid=web.input().get("follow")
    if myuid==str(User.objects(ID=foid).first().id):
        return "not_allowed"
    print str(myuid)==str(User.objects(ID=foid).first().id)
    user=User.objects(id=myuid).first()
    thisguy=User.objects(ID=int(foid)).first()
    if thisguy.ID not in user.followings:
        ids=user.followings
        ids.append(thisguy.ID)
        user.ids=ids
        user.followings_count+=1
        thisguy.followed_count+=1
        user.save()
        thisguy.save()
        return "success"
    return "failed"


                   
class Unfollow:
  @authenticate
  def POST(self):
    unfoid=web.input().get("unfollow")
    thisguy=User.objects(ID=int(unfoid)).first()
    user=User.objects(id=Auth.uid()).first()
    followings=user.followings
    _id=int(unfoid)
    if _id in followings:
       followings.remove(_id)
       user.followings=followings
       user.followings_count-=1
       thisguy.followed_count-=1
       user.save()
       thisguy.save()
       return "Unfollow_success"
    return "cant unfollow"
   
class Followings:
  def GET(self,uid):
      #关注的人
      if Auth.is_login():
             me=User.objects(id=Auth.uid()).first()
      else:
             me=None
      user=User.objects(ID=int(uid)).first()
      followings_ids=user.followings
      followings=[User.objects(ID=idd).first() for idd in followings_ids] 
      page=int(web.input().get("page","1"))
      count=user.followings_count
      if page*10<count:
         next=page+1
      else:
         next=None      
      return  render.followings(user=me,thisguy=user,count=count,next=next,followings=followings)
    
class Followeds:
  def GET(self,uid):
      #关注我的人 should keep it in  a list ?
      if Auth.is_login():
              me=User.objects(id=Auth.uid()).first()
      else:
             me=None
      user=User.objects(ID=int(uid)).first()
      followeds=User.objects(followings=user.ID)
      page=int(web.input().get("page","1"))
      count=user.followed_count
      if page*10<count:
         next=page+1
      else:
         next=None      
      return render.followeds(user=me,thisguy=user,count=count,next=next,followeds=followeds)
