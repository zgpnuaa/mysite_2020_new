# _*_ encoding: utf-8 _*_
import hashlib
import time
import random
import urllib.request as urllib2
import demjson
import string

import django.utils.timezone as timezone

from .models import WxToken, JsToken


def getSignPackage(request):
    # 获得jsapi_ticket
    jsapiTicket = getJsApiTicket()

    # 注意 URL 一定要动态获取，不能 hardcode.
    # 获取当前页面的url
    url = 'http://' + request.get_host() + request.get_full_path()
    print(url)
    # 获取timestamp（时间戳）
    timestamp = int(time.time())
    # 获取noncestr（随机字符串）
    nonceStr = createNonceStr()

    # 这里参数的顺序要按照 key 值 ASCII 码升序排序
    # 得到signature
    # $signature = hashlib.sha1(string).hexdigest();
    ret = {
        'nonceStr': nonceStr,
        'jsapi_ticket': jsapiTicket,
        'timestamp': timestamp,
        'url': url
    }

    string = '&'.join(['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)])
    signature = hashlib.sha1(string.encode(encoding='UTF-8', errors='strict')).hexdigest()

    signPackage = {
        "appId": 'wxb50bc8921024a508',
        "nonceStr": nonceStr,
        "timestamp": timestamp,
        "url": url,
        "signature": signature,
        "rawString": string
    }
    return signPackage


def createNonceStr(length=16):
    # 获取noncestr（随机字符串）
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))


def getJsApiTicket():
    # 获得jsapi_ticket
    # 获得jsapi_ticket之后，就可以生成JS-SDK权限验证的签名了
    # 获取access_token
    try:
        ticket = WxToken.objects.all()[0]
        if ticket.get_date():
            return ticket.token
    except:
        ticket = WxToken()

    accessToken = accesstokens()

    # 获取jsapi_ticket
    url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi".format(accessToken)

    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    res = demjson.decode(res)
    ticket.token = str(res['ticket'])
    ticket.lifetime = timezone.now()
    ticket.save()

    return str(res['ticket'])




def accesstokens():
    try:
        accesstoken = JsToken.objects.all()[0]
        if accesstoken.get_date():
            return accesstoken.token
    except:
        accesstoken = JsToken()

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxb50bc8921024a508&secret=640e3b72541dc38a17db9d10a4b5394e'

    req = urllib2.Request(url)
    print("pppp")
    print(req)
    data = urllib2.urlopen(req)
    print(data)
    res = data.read()
    res = demjson.decode(res)
    print(res)

    accesstoken.token = str(res['access_token'])
    accesstoken.lifetime = timezone.now()
    accesstoken.save()

    return str(res['access_token'])

