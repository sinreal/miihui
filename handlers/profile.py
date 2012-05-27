#coding:utf-8


#from web.contrib.template import render_jinja
import web
from models.user import *
from lib.kit import Auth
from lib.common import render
from lib.decorators import authenticate	
from PIL import Image



class Profile:
     @authenticate
     def GET(self):
            uid=Auth.uid()
            user=User.objects(id=uid).first()
            return render.profile(is_login=True,user=user)
        
     @authenticate
     def POST(self):
            uid=Auth.uid()
            intro=web.input().get("intro")
            user=User.objects(id=uid).first()
            if intro!=user.intro:
                user.intro=intro                      
            user.save()    
            return  render.profile(is_login=True,user=user,content=u"更新信息成功")


class  Profile_password:
     @authenticate
     def GET(self):
            uid=Auth.uid()
            user=User.objects(id=uid).first()
            
            return render.profile_password(is_login=True,user=user)
        
     @authenticate
     def POST(self):
            uid=Auth.uid()
            passwd=web.input().get("password")
            passwd1=web.input().get("password1")
            user=User.objects(id=uid).first()
            if passwd and (passwd!=passwd1):
                return render.profile_password(is_login=True,user=user,content=u"两次密码不同，请再次输入")
            return  render.profile_password(is_login=True,user=user,content=u"更新密码成功")
           



class  Profile_avatar:
    
     @authenticate
     def GET(self):
            uid=Auth.uid()
            user=User.objects(id=uid).first()
            
            return render.profile_avatar(is_login=True,user=user)
        
     @authenticate
     def POST(self):
            uid=Auth.uid()
            user=User.objects(id=uid).first()
            _file= web.input(avatar={})
            if _file['avatar'].filename!="" and  _file['avatar'].filename[-3:]=="jpg":
                  fileimg=_file['avatar'].value 
                  _filename=TEMP+"/"+str(user.ID)+".jpg"
                  open(_filename,"wb").write(fileimg)
                  im = Image.open(_filename)
                  (width,height)=im.size
                  if width<=height:
                    im_new=im.resize((100,int(height*100.0/width)),Image.ANTIALIAS)
                    im_new.transform((100,100),Image.EXTENT ,(0,0,100,100),Image.BILINEAR).save('m'+uid+".jpg",quality = 95)
                    im_new.transform((50,50),Image.EXTENT,(0,0,100,100)).save(STATIC_FILE+'/s'+uid+".jpg",quality = 95)
                    im_new.save(STATIC_FILE+'/b'+uid+".jpg",quality = 95)   
                  else:    
                    im_new=im.resize((int(width*100.0/height),100))
                    im_new.transform((100,100),Image.EXTENT,(0,0,100,100),Image.BILINEAR).save('m'+uid+".jpg",quality = 95)
                    im_new.transform((50,50),Image.EXTENT,(0,0,100,100)).save(STATIC_FILE+'/s'+uid+".jpg",quality = 95)
                    im_new.save(STATIC_FILE+'/b'+uid+".jpg",quality = 95)
                  user.avatar="s"+uid+".jpg"
                  user.avatar_big="b"+uid+".jpg"                          
                  user.save()
            else:
                render.profile_avatar(is_login=True,user=user,content=u"请上传JPG文件")      
            return  render.profile_avatar(is_login=True,user=user,content=u"更新头像成功")

