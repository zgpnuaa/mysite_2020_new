from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from .api import MessageModelViewSet, UserModelViewSet, UserInfoViewSet
from .views import PrivateLetterView
from django.conf.urls import url

app_name = 'chat'

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, base_name='message-api')
router.register(r'user', UserModelViewSet, base_name='user-api')
router.register(r'userinfo', UserInfoViewSet, base_name='userinfo-api')

urlpatterns = [
    re_path('(?P<recipient>[-\w]+)/api/v1/', include(router.urls)),
    re_path('api/v1/', include(router.urls)),
    re_path('(?P<recipient>[-\w]+)/$', PrivateLetterView.as_view(template_name='chat/privateletter.html'), name='privateletter'),
    re_path('', login_required(TemplateView.as_view(template_name='chat/chat.html')), name='friendchat'),

    # re_path('', login_required(
    #     TemplateView.as_view(template_name='chat/kefu_index.html')), name='friendchat'),
]
