#!/usr/bin/python2.6
#coding:utf-8
import web
import hashlib,random
from PIL import Image
import os,sys, time

sys.path.append('../') 

from models.models import *
from lib.time_format import friendly_time
from web.contrib.template import render_jinja

from config import options

ADMIN_LIST=["sinreal@163.com"]


STATIC_FILE=options.get("static_file","")
TEMP=options.get("temp","")
STATIC_FILE_URL=options.get("static_file_url","")


urls=(
'/' ,'Allusers',
'/login','Login',
'/logout','Logout',

'/user/(.*)/','People',
'/item/(\d+)/','Subject',

'/allusers','Allusers',
'/allposts','Allposts',
'/allitems','Allshares',
'/edituser','Edituser',
'/editpost','Editpost',
'/edititem','Edititem',

'/link2/(.*)','Link2',
'/aboutus','About',
)

web.config.debug = True
web.template.Template.globals['STATIC_FILE_URL']=STATIC_FILE_URL
render = render_jinja('templates_admin',   encoding = 'utf-8',)

render._lookup.globals.update( STATIC_FILE_URL=STATIC_FILE_URL,)

app=web.application(urls,globals())

def authenticate(handler):
  def _check_auth(*args,**kwargs):
      if Auth.is_login():
        return handler(*args,**kwargs)
      else:
        web.seeother("/login")
  return _check_auth


class Auth:
    @staticmethod
    def is_login():
     id=web.cookies().get("adid")
     key=web.cookies().get("adkey")
     if id and key  and key==hashlib.md5(id+"3.1415926linyuangz2012").hexdigest():
        return True
     return False        

    @staticmethod
    def uid():
        if web.cookies().get("adid"):
            return web.cookies().get("adid")		          
     
    @staticmethod
    def set_login(id,nickname,time=0):
     key=hashlib.md5(str(id)+"3.1415926linyuangz2012").hexdigest()    
     web.setcookie('adid',str(id))
     web.setcookie('adkey',key)
     return True

    
    @staticmethod
    def set_logout():
      web.setcookie('adid','',-1)
      web.setcookie('adkey','',-1)
      return True

class Index:
      def GET(self):
        content=''
        if Auth.is_login():
           user=User.objects(id=Auth.uid()).first()
        else:
           user=None
        return render.index(user=user)

class Login:
      def GET(self):
          return render.login(is_login=Auth.is_login())
        
      def POST(self):
           if Auth.is_login():
             user=User.objects(id=Auth.uid()).first()
           else:
             user=None
           email=web.input().get("email")
           passwd=web.input().get("password")
           key=passwd
           user = User.objects(email=email).first()
           if  user.email not in ADMIN_LIST:
               return render.login(is_login=Auth.is_login(),content=u"不是管理员")
           if not user :
               return render.login(is_login=Auth.is_login(),content=u"没有这个用户")
           if user.password==key:
               Auth.set_login(user.id,user.username)
               return web.seeother("/")
           return render.login(user=user,content=u"密码错误")


class Logout:
      @authenticate
      def GET(self):
          Auth.set_logout()
          return render.logout(is_login=False)


class Allusers:
       @authenticate
       def GET(self):
         myuid=Auth.uid()
         user=User.objects(id=myuid).first()
         page=int(web.input().get("page","1"))
         counts=User.objects().count()
         if page*50<counts:
            next=page+1
         elif page*50-counts>50 :
            return  web.notfound()
         else:  
            next=None
         users=User.objects()[(page-1)*50:page*50]      
         return  render.allusers(users=users,user=user)

class Allposts:
      @authenticate
      def GET(self):
          myuid=Auth.uid()
          user=User.objects(id=myuid).first()
          page=int(web.input().get("page","1"))
          counts=Tweet.objects(flag__ne=1).count()
          if page*50<counts:
            next=page+1
          elif page*50-counts>50 :
            return  web.notfound()
          else:  
            next=None
          tweets=Tweet.objects(flag__ne=1).order_by("-ID")[(page-1)*50:page*50]
          datalist=[]
          for t in tweets:
             datalist.append((User.objects(ID=t.AutherID).first(),t))
          return  render.allposts(datalist=datalist,user=user,next=next)


class  Editpost:
        @authenticate
        def GET(self):    
          postid=int(web.input().get("postid"))
          myuid=Auth.uid()
          me=User.objects(id=myuid).first()
          tweet=Tweet.objects(ID=int(postid)).first()
          action=web.input().get("action")
          if action=="del":
              tweet.flag=-1
          if action=="showinfont":
               pass
          tweet.save()     
          return render.info(user=me,content=u"成功")

        
class Edituser:  
      @authenticate
      def GET(self):
          #todo 需要一个封杀管理表，另外已经封杀的用户不能发言
          uid=int(web.input().get("uid"))
          myuid=Auth.uid()
          me=User.objects(id=myuid).first()
          thisguy=User.objects(ID=uid).first()
          if  me==thisguy:
              return render.info(is_login=True,user=me,content=u"不能编辑自己")
          action=web.input().get("action")
          if action=="block":
              thisguy.role=1
          elif action=="kill":
               thisguy.role=0
          elif action=="unblock":
               thisguy.role=2
          thisguy.save()     
          return render.info(user=me,content=u"成功")


class  Allshares:
      @authenticate 
      def GET(self):
         myuid=Auth.uid()
         user=User.objects(id=myuid).first()
         page=int(web.input().get("page","1"))
         counts=Node.objects().count()
         if page*50<counts:
            next=page+1
         elif page*50-counts>50 :
            return  web.notfound()
         else:  
            next=None
         nodes=Node.objects().order_by("-ID")[(page-1)*50:page*50]
         return  render.allshares(nodes=nodes,user=user,next=next)



class People:
  @authenticate	
  def GET(self,uid):
      myuid=Auth.uid()
      page=int(web.input().get("page","1")) 
      thisguy=User.objects(ID=int(uid)).first()   
      counts = thisguy.followings_count,thisguy.followed_count,thisguy.tweet_count
      if page*20<counts[2]:
         next=page+1
      elif page*20-counts[2]>20 :
         return  web.notfound()
      else:  
         next=None
      me=User.objects(id=myuid).first()
      if me==thisguy:
            relation="self"
      elif  thisguy.ID in me.followings:
            relation="ifollowhim"
      else:
           relation=None
      # do i follow that people?
      datalist=[]
      #todo 查询需要改正
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

class Home: 
  @authenticate
  def GET(self):
      myuid=Auth.uid()
      page=int(web.input().get("page","1")) 
      me=User.objects(id=myuid).first()
      counts = me.followings_count,me.followed_count,me.tweet_count
      if page*20<counts[2]:
         next=page+1
      elif page*20-counts[2]>20 :
         return  web.notfound()
      else:  
         next=None
      datalist=[]
      posts=Tweet.objects(AutherID=me.ID).order_by("-ID")[(page-1)*20:page*20]

      for p in posts:
          if p.SubjectID>0:
              if p.flag==1:
                   datalist.append(("share" ,Node.objects(ID=p.SubjectID).first(),p, friendly_time(p.created).decode("utf-8")))  
              else:
                  datalist.append(("comment" ,Node.objects(ID=p.SubjectID).first(),p, friendly_time(p.created).decode("utf-8")))
          else:
              datalist.append(("say",p,friendly_time(p.created).decode("utf-8")))
              
      return render.home(is_login=True,datalist=datalist,user=me,counts=counts,next=next)


    
class Edititem:
   @authenticate
   def GET(self):
       pass
   @authenticate
   def POST(self):
      pass


class Tags:
      @authenticate
      def GET(self,tag):
          page=int(web.input().get('page','1'))
          tag=tag.encode('utf-8')
          nodes=Node.objects(tags=tag)
          count=nodes.count()
          if int(page)*10<count:
            next=page+1
          else:
            next=None
          results=[x for x in nodes]
          return render.tags(Auth,tag,results,count,next)  
        
        
class  Subject:
      @authenticate
      def GET(self,id):
         page=int(web.input().get('page','1'))
         item=Node.objects(ID=int(id)).first()
         comments=Tweet.objects(Q(SubjectID=int(id))&Q(flag__ne=1)).order_by("-ID") 
         #flag=1 means share 
         next=None
         if Auth.is_login():
              user=User.objects(id=Auth.uid()).first()
         else:
             user=None
         if item and  item.creatorID:
             creator=User.objects(ID=item.creatorID).first()
         else:
             creator =None
         datalist=[]
         for comment in comments:
            datalist.append((User.objects(ID=comment.AutherID).first(),comment))
         return render.item(user=user,creator=creator,item=item,datalist=datalist)
          

class  Explore:
     @authenticate
     def GET(self):
         nodes=Node.objects().order_by("-ID")
         if Auth.is_login():
              user=User.objects(id=Auth.uid()).first()
         else:
             user=None
         if nodes.count()>20:
             nodes=nodes[0:20]
         return render.explore(user=user,nodes=nodes)


class Search:
      def GET(self):
        return "still coding hard"

class Link2:
      @authenticate 
      def GET(self,url):
          query=web.ctx.query
          if url.startswith("http"):  
            web.seeother(url+query)
          else:
              return render.page404()
            
class About:
      @authenticate
      def GET(self):
        return render.about(is_login=Auth.is_login(),user=None)
          
if __name__=='__main__':
      app.run()     
      
