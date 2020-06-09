from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView, TemplateResponseMixin
from braces.views import LoginRequiredMixin
from account.models import UserInfo, User


class PrivateLetterView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = '/account/new-login'
    template_name = 'chat/privateletter.html'
    print('66665')

    def get(self, request, recipient, **kwargs):
        userinfo_sendto = UserInfo.objects.filter(user=request.user)[0]
        friend_sendto = User.objects.filter(username=recipient)[0]
        userinfo_sendto.friends.add(friend_sendto)

        user_receive = User.objects.filter(username=recipient)[0]
        userinfo_receive = UserInfo.objects.filter(user=user_receive)[0]
        friend_receive = User.objects.filter(username=request.user)[0]
        userinfo_receive.friends.add(friend_receive)

        return self.render_to_response({'recipient_now': friend_sendto})

