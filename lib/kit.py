#coding:utf-8
import web
import hashlib
#from config import SMTP_HOST,MAIL_LOGIN,MAIL_PSWD




def pagenator(page,num,count=20):
    """a pagenator"""
    prev = int(page)-1 == 0 and '1' or str(int(page)-1)
    next = int(page)+1 <= (num-1)/count+1 and str(int(page)+1) or page
    end = str((num-1)/count+1)
    pages = [prev,next,end,page]
    left = min(4,int(page)-1)
    right = min(4,int(end)-int(page))
    if left < 4:
             right = min(8-left,int(end)-int(page))
    if right < 4:
             left = min(8-right,int(page)-1)
    while left > 0:
            pages.append(str(int(page)-left))
            left -= 1
    j = 0
    while j <= right:
        pages.append(str(int(page)+j))
        j += 1
    return pages


class Auth:
    @staticmethod
    def is_login():
     id=web.cookies().get("id")
     key=web.cookies().get("key")
     if id and key  and key==hashlib.md5(id+"linyuangz2011").hexdigest():
        return True
     return False
        

    @staticmethod
    def uid():
        if web.cookies().get("id"):
            return web.cookies().get("id")		          
     
    @staticmethod
    def set_login(id,nickname,time=0):
     key=hashlib.md5(str(id)+"linyuangz2011").hexdigest()    
     web.setcookie('id',str(id))
     web.setcookie('key',key)
     return True
    
    @staticmethod
    def set_logout():
      web.setcookie('id','',-1)
      web.setcookie('key','',-1)
      web.setcookie('nickname','',-1)
      return True


