#coding:utf-8

import time
from models.task import Task
from lib.mail  import sendmail
from datetime import datetime
def addjob(jobtype,jobdetail):
      job=Task(jobtype=jobtype,jobdetail=jobdetail)
      job.save()

               
def  send_verify_mail(mail_to=""):
       #验证地址是邮箱加一个邮箱+一串值 的md5
       s='你好，收到这封邮件是因为你的邮箱注册了觅汇.\n'
       s=s+'点击这里验证你在觅汇的邮箱.'
       sendmail(u"觅汇邮箱验证",s, mail_to)


if __name__=='__main__':
 while 1:
   jobs=Task.objects(result__lt=1)# <! and >-2
   if len(jobs)>0:
      for job in jobs:
           if job.jobtype==1:
              if job.result<-2:
                   break
              mail=job.jobdetail
              try:
                send_verify_mail(mail_to=mail)
                job.result=1
                job.save()
                print datetime.now(),"send mail %s job done"%mail
              except Exception, e:
                print datetime.now(),"send mail %s failed; %s" % (mail,str(e) )
                job.result-=1
                job.save()
              
   else:
      pass
 
   time.sleep(3)
