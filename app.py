#!/usr/bin/python2.6
#coding:utf-8
import web

from handlers.profile import *
from handlers.auth    import *
from handlers.item    import *
from handlers.user    import *
from lib.kit import  Auth
from lib.time_format import friendly_time
from lib.decorators import authenticate
from lib.common import render
from config import *
import json


urls=(
'/' ,'Index',
'/login','Login',

'/logout','Logout',
'/signup','Signup',
'/auth/(.*)','Auth_3d',
'/callback/(.*)','Auth_3d_callback',
'/profile','Profile',
'/profile/password','Profile_password',
'/profile/avatar','Profile_avatar',

'/share_bm','Share_bm',
'/share','Share',
'/explore','Explore',
'/collect','Collectby',

'/edittitle','Edittitle',
'/addtag','Addtag',
'/user/(\d+)/collections/','Usercollections',


'/user/(\d+)/share/','Usershareitems',
'/user/(.*)/','People',
'/(\d+)/followings/','Followings',
'/(\d+)/followeds/','Followeds',
'/follow','Follow',
'/unfollow','Unfollow',
'/home','Home',
'/showinfont','Showinfont',
'/mentions/','Mentions',
'/item/(\d+)/','Subject',
'/comment/','Comment',
'/tags/(.*)','Tags',
'/search/$', 'Search',

'/link2/(.*)','Link2',
'/tools','Tools',
'/aboutus','About',
)

web.config.debug = True


app=web.application(urls,globals())


class Index:
      def GET(self):
        if Auth.is_login():
           user=User.objects(id=Auth.uid()).first()
        else:
           user=None
        nodes=Node.objects(score=20).order_by("-ID")
        if nodes.count()>20:
             nodes=nodes[0:20]
        return render.index(user=user,nodes=nodes)           


class Home: 
  @authenticate
  def GET(self):
      page=int(web.input().get("page","1")) 
      me=User.objects(id=Auth.uid()).first()
      #todo ..
      me.tweet_count=Tweet.objects(AutherID=me.ID).count()
      counts = me.followings_count,me.followed_count,me.tweet_count
      c= me.nodes_follow
      if not  c:
         collections=[]
      else:
          collections=[]
          #取最新的收藏
          for _id in c:
            collections.append(Node.objects(ID=_id).first())
      if len(collections)>6:
         collections=collections[0:6]
      print counts[2]   
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
              
      return render.home(datalist=datalist,user=me,counts=counts,next=next,collections=collections)


from models.share_items import Share_items
class Usershareitems:
    def GET(self,uid): 
      if Auth.is_login():
          user=User.objects(id=Auth.uid()).first()
      else:
          user=None
      thisguy=User.objects(ID=uid).first()    
      datalist=[]    
      shares=Share_items.objects(creatorID=int(uid))
      counts=(0,0,0)
      for p in shares:
             datalist.append(("share" ,Node.objects(ID=p.itemID).first(),p, friendly_time(p.created).decode("utf-8")))
      return render.share_items(user=user,thisguy=thisguy,datalist=datalist,counts=counts)
          


class  Usercollections:
     def GET(self,userID):
       thisguy=User.objects(ID=userID).first()
       c= thisguy.nodes_follow
       if not  c:
         collections=[]
       else:
          collections=[]
          #取最新的收藏
          for _id in c:
            collections.append(Node.objects(ID=_id).first())
       if Auth.is_login():
              me=User.objects(id=Auth.uid()).first()
       else:
             me=None
       counts = thisguy.followings_count,thisguy.followed_count,thisguy.tweet_count      
       return render.usercollections(user=me,thisguy=thisguy, collections=collections, counts =counts)
      
class Comment:
      def GET(self,subjectID):
          pass
        
      @authenticate                 
      def POST(self):
          user=User.objects(id=Auth.uid()).first()
          if user.role!=2:
              return "blocked"
          content=web.input().get('txt')
          typet=web.input().get('type')
          subtopID=int(web.input().get('stID','0'))
          if not content:
             return "Content_empty"
          if typet=="post":
              tweet=Tweet(ID=Tweet.objects.count()+101,AutherID=user.ID,SubjectID=subtopID,content=content)
              user.tweet_count+=1
              tweet.save()
              user.save()
          return "Success"

class  Showinfont:
       @authenticate
       def POST(self):
         url=web.input().get("url")
         itemID=url.split("/")[-2]    
         value=web.input().get("new_value")
         item=Node.objects(ID=int(itemID)).first()
         if value=="yes":
               item.score=20
         elif value=="no":
               item.score=0
         item.save()      
         result={"is_error":"false","error_text":"","html":"done"}
         result_json=json.dumps(result)
         return result_json


class Edittitle:
      @authenticate
      def  POST(self):
            url=web.input().get("url")
            itemID=url.split("/")[-2]
            new_value=web.input().get("new_value")
            item=Node.objects(ID=int(itemID)).first()
            item.name=new_value
            item.save()
            result={"is_error":"false","error_text":"","html":new_value}
            result_json=json.dumps(result)
            return result_json


class Addtag:
      @authenticate
      def  POST(self):
            #item.name=new_value
            #item.save()
            #print web.input()
            itemid=int(web.input().get("itemid"))
            tag=web.input().get("tag")
            item=Node.objects(ID=itemid).first()
            tags=item.tags
            print tags
            if tag not in tags:
               tags.append(tag)
               item.tags=tags   
               item.save()
            print "item saved"
            return "done"



class Collectby:
      @authenticate 
      def  POST(self):
           user=User.objects(id=Auth.uid()).first()
           itemid=web.input().get("itemid")
           # print itemid
           #数据结构为 item，收藏此item的ID
           c=Collect.objects(ID=int(itemid))
           if len(c)!=0:
               c.update_one(push__userlist=user.ID)
               user.update(push__nodes_follow=int(itemid))
               user.save()
               c.first().save()
           else:
              c=Collect(ID=user.ID,userlist=[itemid])
              user.update(push__nodes_follow=int(itemid))
              user.save()
              c.save()
           return None


class Search:
      def GET(self):
        return "still coding hard"

class Link2:
      def GET(self,url):
          query=web.ctx.query
          if url.startswith("http"):  
            web.seeother(url+query)
          else:
              return render.page404()
class  Tools:
       def GET(self):
         return render.tools(is_login=Auth.is_login(),user=None)

class About:
      def GET(self):
        return render.about(is_login=Auth.is_login(),user=None)
          
if __name__=='__main__':
     if DEPLOY:
       web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)  
       app.run()     
     else:
        app.run() 
