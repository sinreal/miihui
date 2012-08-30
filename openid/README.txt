新浪微博API OAuth 2 Python客户端
最新源码
http://code.google.com/p/sinaweibopy/source/browse/src/weibo.py

使用简介
注册微博App后，可以获得app key和app secret，然后定义网站回调地址：

from weibo import APIClient

APP_KEY = '1234567' # app key
APP_SECRET = 'abcdefghijklmn' # app secret
CALLBACK_URL = 'http://www.example.com/callback' # callback url
在网站放置“使用微博账号登录”的链接，当用户点击链接后，引导用户跳转至如下地址：

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()
# TODO: redirect to url
用户授权后，将跳转至网站回调地址，并附加参数code=abcd1234：

# 获取URL参数code:
code = your.web.framework.request.get('code')
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)
access_token = r.access_token # 新浪返回的token，类似abc123xyz456
expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
# TODO: 在此可保存access token
client.set_access_token(access_token, expires_in)
然后，可调用任意API：

print client.get.statuses__user_timeline()
print client.post.statuses__update(status=u'测试OAuth 2.0发微博')
print client.upload.statuses__upload(status=u'测试OAuth 2.0带图片发微博', pic=open('/Users/michael/test.png'))
API调用规则
首先查看新浪微博API文档，例如：

API：statuses/user_timeline

请求格式：GET

请求参数：

source：string，采用OAuth授权方式不需要此参数，其他授权方式为必填参数，数值为应用的AppKey。

access_token：string，采用OAuth授权方式为必填参数，其他授权方式不需要此参数，OAuth授权后获得。

uid：int64，需要查询的用户ID。

screen_name：string，需要查询的用户昵称。

（其它可选参数略）

调用方法：将API的“/”变为“__”，并传入关键字参数，但不包括source和access_token参数：

r = client.get.statuses__user_timeline(uid=123456)
for st in r.statuses:
    print st.text
若为POST调用，则示例代码如下：

r = client.post.statuses__update(status=u'测试OAuth 2.0发微博')
若为上传调用（Multipart Post），传入file-like object参数，示例代码如下：

f = open('/Users/michael/test.png')
r = client.upload.statuses__upload(status=u'测试OAuth 2.0带图片发微博', pic=f)
f.close() # APIClient不会自动关闭文件，需要手动关闭
考虑到大部分调用是GET操作，get可省略，例如，以下两种写法是等价的：

r = client.statuses__user_timeline(uid=123456)
r = client.get.statuses__user_timeline(uid=123456)
使用限制
仅支持Web方式调用，不支持口令方式验证。

补充说明
所有API调用均为动态调用，需要根据新浪API文档由HTTP调用方式（GET，POST或POST Multipart）决定APIClient的属性（get，post或upload），方法名（新浪微博API名称替换“/”为“__”），以及关键字参数。

若调用出错，会抛出APIError异常，该异常包含error_code，error和request三个字段，与新浪返回的出错json对应。具体错误原因请查询新浪文档。

若HTTP响应出错（例如404），会抛出urllib2.HTTPError异常。