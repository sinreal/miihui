#coding:utf-8

import web
import urllib2
from models.node import Node,Buy_info
from models.user import User
from models.models import *
from models.share_items  import Share_items
from lib.kit import Auth
from lib.common import render
from lib.tools import get_store,cut_item_picture
from lib.decorators import authenticate
from lib.upyun import UpYun,md5,md5file
from  config import TEMP,STATIC_FILE,BUCKETNAME,USER,PASSWORD




class Tags:
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
      def GET(self,id):
         page=int(web.input().get('page','1'))
         item=Node.objects(ID=int(id)).first()
         #todo 分页 or ajax
         comments=Tweet.objects(Q(SubjectID=int(id))&Q(flag__ne=1)).order_by("-ID") 
         #flag=1 means share 
         next=None
         if Auth.is_login():
              user=User.objects(id=Auth.uid()).first()
              mycollect=user.nodes_follow
              if item.ID in mycollect:
                 collected=True
              else:
                collected=False
         else:
              user=None
              collected=False
         if item and  item.creatorID:
             creator=User.objects(ID=item.creatorID).first()
         else:
             creator =None
         datalist=[]
         for comment in comments:
            datalist.append((User.objects(ID=comment.AutherID).first(),comment))
         if user==creator :
                 editble=True
         else:
                editble=False
         if  user and ( user.email=="sinreal@163.com" or user.email=="dinghan1987@126.com"  ):
                 editble=True
         return render.item(editble=editble,user=user,creator=creator,item=item,datalist=datalist,collected=collected)
          
class  Share:
       @authenticate  
       def GET(self):
           user=User.objects(id=Auth.uid()).first()  
           if web.input().get("count",None):             
                count=web.input().get("count",None)
                piclist=[]
                for i in range(int(count)):
                     piclist.append(web.input().get("u"+str(i)))
                title=web.input().get("title")
                #print title
                url=web.input().get("fromurl")
                store=get_store(url).decode("utf-8")
                des=web.input().get("d",None)
                return render.share_bm(user=user,piclist=piclist,store=store,title=title,url=url,des=des)
           return render.share(is_login=True,user=user)

       @authenticate                       
       def POST(self):   
           
           name=web.input().get("name")
           _tags=web.input().get("tags")
           source=web.input().get("source")                 
           if _tags:
                tags=[x for x in  _tags.split(",")]
           else:
                tags=[]
           user=User.objects(id=Auth.uid()).first()     
           creatorID=user.ID     
           intro=web.input().get("intro")
           picurl=web.input().get("picurl",None)
           price=web.input().get("price")
           link=web.input().get("source")
           store=get_store("store")
           price=web.input().get("price")
           buyinfo=Buy_info(link=link,store=store,price=price)
           #check if none 
           pic=urllib2.urlopen(picurl).read()
           ID=Node.objects.count()+1
           open(str(ID)+".jpg","wb").write(pic)
           u = UpYun(BUCKETNAME,USER,PASSWORD)
           data = open(str(ID)+".jpg",'rb')
           u.setContentMD5(md5file(data))
           a = u.writeFile('/o'+str(ID)+'.jpg',data)
           if not a:
             return "get picture erro"
           #cut_item_picture(STATIC_FILE,ID,str(ID)+".jpg")  
           node=Node(creatorID=creatorID,ID=ID,name=name,des=intro,picurl=picurl,tags=tags,buy_info=[buyinfo])
           node.picinfo=101    #a out sidelink
           node.save()
           share=Share_items(ID=Share_items.objects.count()+1,creatorID=user.ID,itemID=ID,flag=1,content="")
           share.save()
           #加入到shareitem中
           #todo count更新
           tweet=Tweet(ID=Tweet.objects.count()+1,AutherID=user.ID,SubjectID=ID,flag=1,content=str(ID))
           tweet.save()
           return web.seeother("/item/"+str(ID)+"/")


class Share_bm:
      def GET(self):
          pass
        
      @authenticate  
      def POST(self):
               picurl=web.input().get("check")
               name=web.input().get("name")
               _tags=web.input().get("tags")
               source=web.input().get("source")                 
               if _tags:
                 tags=[x for x in  _tags.split(",")]
               else:
                 tags=[]
               user=User.objects(id=Auth.uid()).first()     
               creatorID=user.ID     
               intro=web.input().get("intro")
               price=web.input().get("price")
               link=web.input().get("source")
               store=web.input().get("store")
               #store=get_store(link).decode("utf-8")
               price=web.input().get("price")
               buyinfo=Buy_info(link=link,store=store,price=price)
               pic=urllib2.urlopen(picurl).read()
               ID=Node.objects.count()+1
               open(str(ID)+".jpg","wb").write(pic)
               u = UpYun(BUCKETNAME,USER,PASSWORD)
               data = open(str(ID)+".jpg",'rb')
               u.setContentMD5(md5file(data))
               a = u.writeFile('/o'+str(ID)+'.jpg',data)
               if not a:
                   return "get picture erro"
               #cut_item_picture(STATIC_FILE,ID,str(ID)+".jpg")  
               node=Node(creatorID=creatorID,ID=ID,name=name,des=intro,picurl=picurl,tags=tags,buy_info=[buyinfo])
               node.picinfo=101    #a out sidelink
               node.save()
               share=Share_items(ID=Share_items.objects.count()+1,creatorID=user.ID,itemID=ID,flag=1,content="")
               share.save()
               content=u'''<h1>发布成功</h1><p>你可以<a href="/item/%s/">去看看</a>或者
               <a href="%s">回到刚才的逛的</a>'''%(str(ID),source)
               return render.info(content=content)
               return web.seeother("/item/"+str(ID)+"/")
            

        

class  Explore:
     def GET(self):
         nodes=Node.objects(score=20).order_by("-ID")
         if Auth.is_login():
              user=User.objects(id=Auth.uid()).first()
         else:
             user=None
         if nodes.count()>20:
             nodes=nodes[0:20]
         return render.explore(user=user,nodes=nodes)
