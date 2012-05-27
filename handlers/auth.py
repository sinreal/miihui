#coding:utf-8

import web
from models.user import *
from models.models import *
from lib.kit import Auth
from lib.decorators import authenticate	
from lib.common import render
from  openid.weibo import APIClient

from config import APIKEY_DICT 
APP_KEY=APIKEY_DICT["sina"].get("key") 
APP_SECRET=APIKEY_DICT["sina"].get("secret") 
CALLBACK_URL=APIKEY_DICT["sina"].get("redirect_uri") 




class Signup:
      def GET(self):
          return render.signup(is_login=Auth.is_login(),content=None) 

      def POST(self):
         email=web.input().get("email")
         name=web.input().get("nickname")
         passwd=web.input().get("password")
         if not( email and name and passwd):
               content= u"输入不能为空"
               return render.signup(is_login=False,content=content)  
         if  User.objects(email=email).first() :
               content= u"邮箱已经注册"
               return render.signup(is_login=False,content=content) 
         if   User.objects(username=name).first() :
               content =u"用户名已经被注册"
               return render.signup(is_login=False,content=content) 
         ID=User.objects.count() + 101
         user = User(username=name,email=email,password=passwd,ID=User.objects.count() + 101)
         user.avatar="default.png"
         user.avatar_big="default_big.png"
         #方便管理，只有一级目录
         user.save()
         if user : 
            Auth.set_login(user.id,name.encode("utf-8"))
            return web.seeother("/")
         else:
               content =u"用户名已经被注册"
               return render.signup(is_login=False,content=content)
"""           
class Email_verify:
      def GET(self):
         email=web.input().get("email")
         code=web.input().get("code")
         if  Verifyemail.verify(email,code):
              u=User.find_by_email(email)
              Auth.set_login(user.id,name.encode("utf-8"))
              return render.profilling(Auth,content="welcome")
         return render.email_verify(Auth,content="email_verify_failed")   
"""          
class Login:
      def GET(self):
          return render.login(is_login=Auth.is_login())
        
      def POST(self):
           email=web.input().get("email")
           passwd=web.input().get("password")
           key=passwd
           #key=hashlib.md5(passwd).hexdigest()
           user = User.objects(email=email).first()
           if not user :
               return render.login(is_login=Auth.is_login(),content=u"没有这个用户")
           if user.password==key:
               Auth.set_login(user.id,user.username)
               return web.seeother("/")
           return render.login(is_login=Auth.is_login(),content=u"密码错误")


class Logout:
      @authenticate
      def GET(self):
          Auth.set_logout()
          return render.logout(is_login=False)


class Auth_3d:
     def GET(self,provider):
       if provider!="sina":
          return u"todo"
       client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
       url = client.get_authorize_url()
       content=u'<h1>功能测试中</h1><p>请联系我们开通您的微博登录功能.</p><a href="%s">继续</a>'%url
       return render.info(content=content)
           
class Auth_3d_callback:
      def GET(self,provider):
        if provider!="sina":
          return "todo"      
        code=web.input().get("code")
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        r = client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in
        client.set_access_token(access_token, expires_in)
        uid =r.uid
        weibouser=client.get.users__show(uid=uid)
        sinaid=weibouser.get("id")
        authbind=Auth_bind.objects(opid="sina"+str(sinaid)).first()
        if authbind==None:
          avatar_large=weibouser.get("avatar_large")
          avatar=weibouser.get("profile_image_url")
          username=weibouser.get("screen_name")
          username=username+"21223"
          #??????          I
          ID=User.objects.count() + 101
          u=User(username=username,email="!!sina2"+str(sinaid),password="",ID=ID)
          u.avatar=avatar
          u.avatar_big=avatar_large
          u.save()
          a=Auth_bind(ID=ID,opid="sina"+str(sinaid),access_token=access_token,expires_in=str(expires_in))
          a.save()
          Auth.set_login(u.id,username.encode("utf-8"))
          return  web.seeother("/")
        else:
           ID=authbind.ID
           user=User.objects(ID=ID).first()
           Auth.set_login(user.id,user.username.encode("utf-8"))
           return web.seeother("/")






