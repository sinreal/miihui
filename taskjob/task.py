#coding:utf-8



from models.task import Task



jobs=Task.objects(result__lt=1)
if len(jobs)>0:
     print "start job"
else:
    print "no job"

