from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserInfoForm, UserInfoForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserInfo
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from article.models import ArticleColumn, ArticlePost
import random
from slugify import slugify
from mysite.settings import MEDIA_ROOT
import os
import base64
from PIL import Image
from io import BytesIO
from social_django.models import AbstractUserSocialAuth
from social_django.models import UserSocialAuth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect, reverse
from urllib import request as request_urllib  # 换个名字以避免与视图函数的request冲突
from django.core.files.base import ContentFile
import logging
import traceback
import imghdr


# Create your views here.


logger = logging.getLogger("django")
collect_logger = logging.getLogger("collect")

def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                login(request, user)
                return HttpResponse("Welcome You. You have been authenticated successfully")
            else:
                return HttpResponse("Sorry. Your username or password is not right.")
        else:
            return HttpResponse("Invalid login.")

    if request.method == "GET":
        collect_logger.info('hello\n')
        logger.info('hello\n')
        logger.info("我是debug")
        logger.info("我是info")
        logger.info("发现一个error")
        collect_logger.info("user1:广东")
        logging.info('66666666666')
        print('666')
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})


def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        #username_rg = user_form.cleaned_data['username']
        username_rg = request.POST.get('username')
        print(username_rg)
        if User.objects.filter(username=username_rg):
            tips = '该用户名已被注册，请换一个用户名。'
            return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form, "tips": tips})
        elif user_form.is_valid()*userprofile_form.is_valid():
            email = user_form.cleaned_data['email']
            birth = userprofile_form.cleaned_data['birth']
            phone = userprofile_form.cleaned_data['phone']
            password1 = user_form.cleaned_data['password']
            password2 = user_form.cleaned_data['password2']
            print(111)
            if password1 != password2:
                tips = '两次输入密码不相同，请重新输入密码。'
                return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form,  "tips": tips})
            elif userprofile_form.errors:
                tips = userprofile_form.errors
                print(tips)
                return render(request, "account/register.html",
                              {"form": user_form, "profile": userprofile_form, "tips": tips})
            else:
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                new_profile = userprofile_form.save(commit=False)
                new_profile.user = new_user
                new_profile.save()
                new_userinfo = UserInfo.objects.create(user=new_user)
                new_userinfo.photo = '/icons/default.png'
                new_userinfo.save()
                # ArticleColumn.objects.create(user=new_user)
                return render(request, "account/register_pagejump.html", {"name": new_user.username})
        else:
            l = len(str(userprofile_form.errors.as_data()['phone'][0]))
            l = l - 2
            tips = str(userprofile_form.errors.as_data()['phone'][0])[2:l]
            print(tips)
            return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form, "tips": tips})
    else:
        collect_logger.info('hello\n')
        logger.info('hello\n')
        logger.info("我是debug")
        logger.info("我是info")
        logger.info("发现一个error")
        collect_logger.debug("user1:广东")
        logging.info('66666666666')
        print('666')
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})


@login_required(login_url='/account/new-login')
def myself(request):
    user = User.objects.get(username=request.user.username)
    if UserProfile.objects.filter(user=user):
        userprofile = UserProfile.objects.filter(user=user)[0]
    else:
        userprofile = UserProfile.objects.create(user=user)
        userprofile.save()
    if UserInfo.objects.filter(user=user):
        userinfo = UserInfo.objects.filter(user=user)[0]
        print(userinfo.photo)
    else:
        userinfo = UserInfo.objects.create(user=user)
        userinfo.save()
    print('iiiii')

    # print(userinfo.photo.url)
    return render(request, "account/myself.html", {"user": user, "userinfo": userinfo, "userprofile": userprofile})


@login_required(login_url='/account/new-login')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    if UserProfile.objects.filter(user=user):
        userprofile = UserProfile.objects.filter(user=user)[0]
    else:
        userprofile = UserProfile.objects.create(user=user)
        userprofile.save()
    if UserInfo.objects.filter(user=user):
        userinfo = UserInfo.objects.filter(user=user)[0]
    else:
        userinfo = UserInfo.objects.create(user=user)
        userinfo.save()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)

        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information')
    else:
        user_form = UserForm(instance=request.user)
        if userprofile:
            userprofile_form = UserProfileForm(initial={"birth": userprofile.birth, "phone": userprofile.phone})
        else:
            userprofile_form = UserProfileForm(initial={"birth": '', "phone": ''})
        if userinfo:
            userinfo_form = UserInfoForm(initial={"school": userinfo.school, "company": userinfo.company, "profession": userinfo.profession, "addresss": userinfo.address, "aboutme": userinfo.aboutme})
        else:
            userinfo_form = UserInfoForm(
                initial={"school": '', "company": '', "profession": '',
                         "addresss": '', "aboutme": ''})

        return render(request, "account/myself_edit.html", {"user_form": user_form, "userprofile_form": userprofile_form, "userinfo_form": userinfo_form, "userinfo": userinfo})


@login_required(login_url='/account/new-login')
def my_image(request):
    if request.method == 'POST':
        img_b64 = request.POST['img']
        img_info = img_b64.split(',')
        suff = img_info[0].split(';')
        suff = suff[0].split('/')
        img_b64decode = base64.b64decode(img_info[1])
        img_data = BytesIO(img_b64decode)
        img = Image.open(img_data)
        url = '/icons/' + slugify(request.user.username) + '-' + 'icon.'+suff[1]
        name = MEDIA_ROOT + '/' + url
        try:
            img.save(name)
            userinfo = UserInfo.objects.get(user=request.user.id)
            userinfo.photo = url
            userinfo.save()
            return HttpResponse("1")
        except Exception as e:
            return HttpResponse("2")
    else:
        return render(request, "account/imagecrop.html")


def SocialAuth(request):
    if request.method == 'POST':
        user =request.POST
        print(user)
        return HttpResponse(" login.")
    if request.method == 'get':
        user = AbstractUserSocialAuth.user
        user_login(request, user)
        #print(user.username)
        return HttpResponse(" login.")

@login_required(login_url='/account/new-login')
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        weibo_login = user.social_auth.get(provider='weibo')
    except UserSocialAuth.DoesNotExist:
        weibo_login = None

    try:
        qq_login = user.social_auth.get(provider='qq')
    except UserSocialAuth.DoesNotExist:
        qq_login = None

    can_disconnect = (user.social_auth.count()>1 or user.has_usable_password())

    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, '您的密码成功更新！')
            return redirect('password')
        else:
            messages.error(request, '请修正以下错误！')
    else:
        form = PasswordForm(request.user)
    print(form)
    return render(request, 'account/settings.html', {'github_login': github_login, 'weibo_login': weibo_login, 'qq_login': qq_login, 'can_disconnect': can_disconnect, 'form': form,})

@login_required(login_url='/account/new-login')
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, '您的密码成功更新！')
            return redirect('password')
        else:
            messages.error(request, '请修正以下错误！')
    else:
        form = PasswordForm(request.user)
    return render(request,  'account/password.html', {'form': form})


def get_userinfo(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        weibo_login = user.social_auth.get(provider='weibo')
    except UserSocialAuth.DoesNotExist:
        weibo_login = None

    try:
        qq_login = user.social_auth.get(provider='qq')
    except UserSocialAuth.DoesNotExist:
        qq_login = None

    if github_login:
        userinfo = github_login.extra_data
        user_github = User.objects.filter(username=userinfo['login'])[0]
        user_profile = UserProfile.objects.filter(user=user_github)
        if user_profile:
            pass
        else:
            newuserprofile = UserProfile.objects.create(user=user_github, phone='', birth='')
            newuserprofile.save()
        user_info = UserInfo.objects.filter(user=user_github)
        if user_info:
            user_info[0].photo = '/icons/github.jpg'
            user_info[0].save()
        else:
            newuserinfo = UserInfo.objects.create(user=user_github)
            newuserinfo.photo = '/icons/github.jpg'
            newuserinfo.save()
    elif weibo_login:
        collect_logger.info('weibo\n')
        userinfo = weibo_login.extra_data
        user_weibo = User.objects.filter(username=userinfo['username'])[0]
        user_profile = UserProfile.objects.filter(user=user_weibo)
        if user_profile:
            pass
        else:
            newuserprofile = UserProfile.objects.create(user=user_weibo, phone='', birth='')
            newuserprofile.save()
        user_info = UserInfo.objects.filter(user=user_weibo)
        collect_logger.info(user_info)
        if user_info:
            try:
                collect_logger.info(userinfo['profile_image_url'])
                url = MEDIA_ROOT+'/icons/' + slugify(request.user.username) + '-' + 'icon'
                response = request_urllib.urlretrieve(userinfo['profile_image_url'], url)
                extension = imghdr.what(url)
                os.rename(url, url+'.'+extension)
                name = '/icons/' + slugify(request.user.username) + '-' + 'icon.' + extension
                collect_logger.info(name)
                collect_logger.debug(response)
                user_info[0].photo = name
            except Exception as e:
                collect_logger.info(traceback.format_exc())
                collect_logger.info('\n')
                collect_logger.info(repr(e))
                user_info[0].photo = '/icons/default.png'
            user_info[0].save()
        else:
            newuserinfo = UserInfo.objects.create(user=user_weibo)
            collect_logger.info(newuserinfo)
            try:
                collect_logger.info('in\n')
                url = MEDIA_ROOT + '/icons/' + slugify(request.user.username) + '-' + 'icon'
                response = request_urllib.urlretrieve(userinfo['profile_image_url'], url)
                extension = imghdr.what(url)
                os.rename(url, url + '.' + extension)
                name = '/icons/' + slugify(request.user.username) + '-' + 'icon.' + extension
                collect_logger.info(name)
                collect_logger.debug(response)
                newuserinfo.photo = name
            except Exception as e:
                collect_logger.info(traceback.format_exc())
                collect_logger.info('\n')
                collect_logger.info(repr(e))
                newuserinfo.photo = '/icons/default.png'
            newuserinfo.save()
    elif qq_login:
        collect_logger.info('qq\n')
        userinfo = qq_login.extra_data
        collect_logger.info(userinfo['username'])
        user_qq = User.objects.filter(first_name=userinfo['username'])[0]
        user_profile = UserProfile.objects.filter(user=user_qq)
        if user_profile:
            pass
        else:
            newuserprofile = UserProfile.objects.create(user=user_qq, phone='', birth='')
            newuserprofile.save()
        user_info = UserInfo.objects.filter(user=user_qq)
        collect_logger.info(user_info)
        if user_info:
            try:
                collect_logger.info(userinfo['profile_image_url'])
                url = MEDIA_ROOT + '/icons/' + slugify(request.user.username) + '-' + 'icon'
                response = request_urllib.urlretrieve(userinfo['profile_image_url'], url)
                extension = imghdr.what(url)
                os.rename(url, url + '.' + extension)
                name = '/icons/' + slugify(request.user.username) + '-' + 'icon.' + extension
                collect_logger.info(name)
                collect_logger.debug(response)
                user_info[0].photo = name
            except Exception as e:
                collect_logger.info(traceback.format_exc())
                collect_logger.info('\n')
                collect_logger.info(repr(e))
                user_info[0].photo = '/icons/default.png'
            user_info[0].save()
        else:
            newuserinfo = UserInfo.objects.create(user=user_qq)
            collect_logger.info(newuserinfo)
            try:
                collect_logger.info('in\n')
                url = MEDIA_ROOT + '/icons/' + slugify(request.user.username) + '-' + 'icon'
                response = request_urllib.urlretrieve(userinfo['profile_image_url'], url)
                extension = imghdr.what(url)
                os.rename(url, url + '.' + extension)
                name = '/icons/' + slugify(request.user.username) + '-' + 'icon.' + extension
                collect_logger.info(name)
                collect_logger.debug(response)
                newuserinfo.photo = name
            except Exception as e:
                collect_logger.info(traceback.format_exc())
                collect_logger.info('\n')
                collect_logger.info(repr(e))
                newuserinfo.photo = '/icons/default.png'
            newuserinfo.save()
    return redirect(reverse('home'))
