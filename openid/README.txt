����΢��API OAuth 2 Python�ͻ���
����Դ��
http://code.google.com/p/sinaweibopy/source/browse/src/weibo.py

ʹ�ü��
ע��΢��App�󣬿��Ի��app key��app secret��Ȼ������վ�ص���ַ��

from weibo import APIClient

APP_KEY = '1234567' # app key
APP_SECRET = 'abcdefghijklmn' # app secret
CALLBACK_URL = 'http://www.example.com/callback' # callback url
����վ���á�ʹ��΢���˺ŵ�¼�������ӣ����û�������Ӻ������û���ת�����µ�ַ��

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()
# TODO: redirect to url
�û���Ȩ�󣬽���ת����վ�ص���ַ�������Ӳ���code=abcd1234��

# ��ȡURL����code:
code = your.web.framework.request.get('code')
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)
access_token = r.access_token # ���˷��ص�token������abc123xyz456
expires_in = r.expires_in # token���ڵ�UNIXʱ�䣺http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
# TODO: �ڴ˿ɱ���access token
client.set_access_token(access_token, expires_in)
Ȼ�󣬿ɵ�������API��

print client.get.statuses__user_timeline()
print client.post.statuses__update(status=u'����OAuth 2.0��΢��')
print client.upload.statuses__upload(status=u'����OAuth 2.0��ͼƬ��΢��', pic=open('/Users/michael/test.png'))
API���ù���
���Ȳ鿴����΢��API�ĵ������磺

API��statuses/user_timeline

�����ʽ��GET

���������

source��string������OAuth��Ȩ��ʽ����Ҫ�˲�����������Ȩ��ʽΪ�����������ֵΪӦ�õ�AppKey��

access_token��string������OAuth��Ȩ��ʽΪ���������������Ȩ��ʽ����Ҫ�˲�����OAuth��Ȩ���á�

uid��int64����Ҫ��ѯ���û�ID��

screen_name��string����Ҫ��ѯ���û��ǳơ�

��������ѡ�����ԣ�

���÷�������API�ġ�/����Ϊ��__����������ؼ��ֲ�������������source��access_token������

r = client.get.statuses__user_timeline(uid=123456)
for st in r.statuses:
    print st.text
��ΪPOST���ã���ʾ���������£�

r = client.post.statuses__update(status=u'����OAuth 2.0��΢��')
��Ϊ�ϴ����ã�Multipart Post��������file-like object������ʾ���������£�

f = open('/Users/michael/test.png')
r = client.upload.statuses__upload(status=u'����OAuth 2.0��ͼƬ��΢��', pic=f)
f.close() # APIClient�����Զ��ر��ļ�����Ҫ�ֶ��ر�
���ǵ��󲿷ֵ�����GET������get��ʡ�ԣ����磬��������д���ǵȼ۵ģ�

r = client.statuses__user_timeline(uid=123456)
r = client.get.statuses__user_timeline(uid=123456)
ʹ������
��֧��Web��ʽ���ã���֧�ֿ��ʽ��֤��

����˵��
����API���þ�Ϊ��̬���ã���Ҫ��������API�ĵ���HTTP���÷�ʽ��GET��POST��POST Multipart������APIClient�����ԣ�get��post��upload����������������΢��API�����滻��/��Ϊ��__�������Լ��ؼ��ֲ�����

�����ó������׳�APIError�쳣�����쳣����error_code��error��request�����ֶΣ������˷��صĳ���json��Ӧ���������ԭ�����ѯ�����ĵ���

��HTTP��Ӧ��������404�������׳�urllib2.HTTPError�쳣��