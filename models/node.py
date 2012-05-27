# -*- coding: utf-8-*-
from config import options
from mongoengine import *
from datetime import datetime

Model=Document
DB=options.get("DB")
connect(DB)

STATIC_FILE_URL=options.get("static_file_url")


UPAIYUNURL="http://imihui.b0.upaiyun.com"

class Buy_info(EmbeddedDocument):                  # class that inherits from 
    link= StringField(max_length=400)         
    store = StringField(max_length=50)
    price=StringField(max_length=20)
    remark=StringField(max_length=100)
    



class  Node(Model):
    """
    picinfo=0 表示未处理，picurl为原始地址 处理后为大图地址
    picinfo=-1 图片处理失败
    picinfo=3 图大于500px
        2 大于220px 小于500
        1 大于120px 小于220
        101 表示在网上
    """    
    ID=IntField(min_value=1,required=True,unique=True)
    name=StringField(max_length=100,required=True)
    maintype=StringField(max_length=20)  
    #uniquename=StringField(max_length=100, unique=True,required=True)
    creatorID=IntField()
    source=StringField(max_length=400)
    tags=ListField(StringField(max_length=20))
    des=StringField(required=True)
    price=StringField()
    buy_info=ListField(EmbeddedDocumentField(Buy_info))
    picurl=StringField()

    picinfo=IntField(min_value=0) 
    folowedby=ListField(IntField())
    created = DateTimeField(default=datetime.now)
    score=IntField(default=20)
    #plus score
    #showinfront=IntField(default=1)
    #修改为flag ，标记是否显示，是否在前台显示
    
    '''
    def get_big_pic(self)
    if picinfo!=0 and picinfo!=:
       return   STATIC_FILE_URL+"/o"+self.ID+".jpg"
    尝试使用又拍云版本
    试图分文件夹使用
    '''
    def get_b_pic(self):
     picinfo=self.picinfo
     if picinfo!=0 and picinfo!=-1:
       return  UPAIYUNURL+'/o' +str(self.ID)+".jpg!big.jpg"
       #return   STATIC_FILE_URL+"/b"+str(self.ID)+".jpg"
    
    
    def get_m_pic(self):
     picinfo=self.picinfo   
     if picinfo!=0 and picinfo!=-1:
       return  UPAIYUNURL+'/o' +str(self.ID)+".jpg!mid.jpg"  
       #return   STATIC_FILE_URL+"/m"+str(self.ID)+".jpg"

    def get_s_pic(self):
     picinfo=self.picinfo   
     if picinfo!=0 and picinfo!=-1:
       return   STATIC_FILE_URL+"/s"+str(self.ID)+".jpg"
