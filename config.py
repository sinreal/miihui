#coding:utf-8

options= {"DB":'imihui',
          "default_gravatar":"",
          "password_secret":"sinreallinyuan",
          "static_file":"/static",
          "static_file_url":"http://imihui.com/static",
          }

TEMP=""
STATIC_FILE_URL=options.get("static_file_url")
STATIC_FILE=options.get("static_file")
SITE="http://imihui.com"


DEPLOY=False


BUCKETNAME="imihui"
USER="sinreal"
PASSWORD="linyuan2009"



SMTP_HOST="smtp.mailgun.org"
SMTP_USERNAME="noreply@imihui.mailgun.org"
SMTP_PASSWORD="linyuan2009"


OPENID_DOUBAN = 'douban'
OPENID_SINA = 'sina'
OPENID_QQ = 'qq' ##qq w`eibo
OPENID_RENREN='renren'

OPENID_TYPE_DICT = {
    OPENID_DOUBAN : "D",
    OPENID_SINA : "S",
    OPENID_QQ : "Q",
    OPENID_RENREN:'R',
}

OPENID_TYPE_NAME_DICT = {
    "D" : u"豆瓣",
    "S" : u"新浪微博",
    "Q" : u"腾讯微博",
    "R": u"人人网",
}

#-- oauth key & secret config --
#注意豆瓣oauth2 的申请地址为https://www.douban.com/service/auth2/apikey/apply
#考虑是否使用1,1暂时支持永久同步
APIKEY_DICT = {
    OPENID_DOUBAN : {
        "key" : "0610e69a90110b6e1232b3cfb033224a",
        "secret" : "06eb9f70fd04cfb5",
        "redirect_uri" : SITE+"/callback",
    },
    OPENID_SINA : {
        "key" : "736157941",
        "secret" : "ea229feaf54fe5ec7e9f9f5e43102651",
        "redirect_uri" : SITE+"/callback/sina",
    },
    OPENID_QQ: {
        "key" : "801118076",
        "secret" : "7f09f4618cd9189d02ee5efecedd7dfb",
        "redirect_uri" : SITE+"/auth/callback",
    },
    OPENID_RENREN: {
        "key" : "942b7d80e2f64e81b18bd6255b742fcf",
        "secret" : "7e7c0cc4c2b24f7c845e95841ef64736",
        "redirect_uri" : SITE+"/auth/callback",
    },

}

#-- category of status --
CATE_DOUBAN_STATUS = 100
CATE_DOUBAN_NOTE = 101
CATE_DOUBAN_MINIBLOG = 102
CATE_DOUBAN_PHOTO = 103
CATE_SINA_STATUS = 200
CATE_WORDPRESS_POST = 300
CATE_QQWEIBO_STATUS = 500

CATE_LIST = (
    CATE_DOUBAN_NOTE,
    CATE_DOUBAN_MINIBLOG,
    CATE_SINA_STATUS,
    CATE_QQWEIBO_STATUS,
)

DOUBAN_NOTE = 'http://douban.com/note/%s'
DOUBAN_MINIBLOG = 'http://douban.com/people/%s/status/%s'
DOUBAN_STATUS = 'http://douban.com/people/%s/status/%s'
WEIBO_STATUS = 'http://weibo.com/%s'
QQWEIBO_STATUS = 'http://t.qq.com/t/%s'

DOUBAN_SITE = "http://www.douban.com"
SINA_SITE = "http://weibo.com"
QQWEIBO_SITE = "http://t.qq.com"
