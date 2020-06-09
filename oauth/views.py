from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from .oauth_client import OAuth_WEIBO
from .models import OAuth_ex
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


import time,uuid

# Create your views here.

def weibo_login(request):
    oauth_weibo = OAuth_WEIBO(settings.WEIBO_APPID, settings.WEIBO_KEY, settings.WEIBO_CALLBACK_URL)
    url = oauth_weibo.get_auth_url()
    return HttpResponseRedirect(url)

def weibo_check(request):
    type = 3
    code = request.GET.get('code', '')
    oauth_weibo = OAuth_WEIBO(settings.WEIBO_APP_ID, settings.WEIBO_KEY, settings.WEIBO_CALBACK_URL)
    try:
        oauth_weibo.get_access_token(code)
        time.sleep(0.1)
    except:
        data = {}
        data['goto_url'] = '/'
        data['goto_time'] = 10000
        data['goto_page'] = "登录失败"
        data['message_title'] = "获取授权失败，请确认是否允许授权，并重试。若问题无法解决，请联系网站管理人员"
        return render_to_response('oauth/response.html', data)
    openid = oauth_weibo.get_open_id()
    weibos = OAuth_ex.objects.filter(openid=openid, type=type)
    if weibos:
        auth_login(request, weibos[0].user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('/')
    else:
        try:
            email = oauth_weibo.get_email()
        except:
            infos = oauth_weibo.get_user_info()
            nickname = infos.get('screenname', '')
            image_url = infos.get('avatar_large', '')
            signature = infos.get('description', '')
            if not signature:
                signature = '无个性签名'
            print('signature=' + signature)
            sex = '2' if infos.get('gender', '') == 'f' else '1'
            url = "%s?nickname=%s&openid=%s&type=%s&signature=%s&image_url=%s&sex=%s" % (reverse('oauth:bind_email'))
            return HttpResponseRedirect(url)
    users = User.objects.filter(email=email)
    if users:
        user = users[0]
    else:
        while User.objects.filter(username=nickname):
            nickname = nickname + '*'
            user = User(username=nickname, email=email, sex=sex, signature=signature)
            pwd = str(uuid.uuid1())
            user.set_password(pwd)
            user.is_active = True
            user.download_image(image_url, nickname)
            user.save()
    oauth_ex = OAuth_ex(user=user, openid=openid, type=type)
    oauth_ex.save()
    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    data = {}
    data['goto_url'] = '/'
    data['goto_time'] = 10000
    data['goto_page'] = True
    data['message_title'] = "绑定用户成功"
    data['messgae'] = u"绑定成功！您的用户名为：<b>%s</b>。您现在可以同时使用本站帐号和此第三方帐号登录本站了！" % nickname
    return render_to_response('oauth/response.htnl', data)
