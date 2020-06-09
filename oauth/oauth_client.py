# 将各种登录方式所需要的方法封装到对应的类中，处理相似的流程，减少代码冗余，方便理解

import json
import urllib
import re

# 基类，将相同的方法写入此类

class Oauth_Base(object):
    # 初始化，载入对应的id，密钥，回调地址
    def __init__(self, client_id, client_key, redirect_url):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    # get方法
    def _get(self, url, data):
        request_url = '%s?%s' % (url, urllib.parse.urlencode(data))
        response = urllib.request.urlopen(request_url)
        return response.read()

    # post方法
    def _post(selfself, url, data):
        request = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(encoding='UTF8'))
        response = urllib.request.urlopen(request)
        return response.read()

    #以下方法，不同登录平台有细微差别，需继承基类后重写方法

    # 获取code
    def get_auth_url(self):
        pass

    # 获取access toen
    def get_access_token(self, code):
        pass

    # 获取openid
    def get_open_id(self):
        pass

    # 获取用户信息
    def get_user_info(self):
        pass

    # 获取用户邮箱
    def get_email(self):
        pass


# 微博类
class OAuth_WEIBO(Oauth_Base):
    def get_auth_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_url': self.redirect_url,
            'scope': 'email',
            'state': 1,
        }
        url = 'https://api.weibo.com/oauth2/authorize?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self, code):
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_key,
            'code': code,
            'redirect_url': self.redirect_url,
        }
        response = self._post('https://api.weibo.com/oauth2/access_token', params)
        result = json.loads(response.decode('utf-8'))
        self.access_token = result['sccess_token']
        self.openid = result['uid']
        return self.access_token

    # 新浪微博的openid在之前get_access_token()方法已获得
    def get_open_id(self):
        return self.openid

    def get_user_info(self):
        params = {
            'access_token': self.access_token,
            'uid': self.openid,
        }
        response = self._get('https://api.weibo.com/2/account/profile/show.json', params)
        result = json.loads(response.decode('utf-8'))
        return result

    def get_email(self):
        params = {'access_token': self.access_token}
        response = self._get('https://api.weibo.com/2/account/profile/email.json', params)
        result = json.loads(response.decode('utf-8'))
        return result[0]['email']

