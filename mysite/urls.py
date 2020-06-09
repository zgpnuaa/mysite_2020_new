"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import serve, static
from django.views.generic import TemplateView
import notifications.urls
from django.views import generic


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('blog/', include('blog.urls', namespace='blog')),
    path('account/', include('account.urls', namespace='account')),
    path('pwd_reset/', include(("password_reset.urls", 'pwd_reset'), namespace='pwd_reset')),
    path('article/', include("article.urls", namespace='article')),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    # set URL for files in media
    #re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('image/', include('image.urls', namespace='image')),
    path('course/', include('course.urls', namespace='course')),
    path('', include('social_django.urls', namespace='social')),
    # path('search/', include('haystack.urls')),
    path('monitor/', include('monitor.urls', namespace='monitor')),
    path('/notifications/', include(notifications.urls, namespace='notifications')),
    path('notice/', include('notice.urls', namespace='notice')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('astrology/', include('astrologychart.urls', namespace='astrology')),
    path('MP_verify_h59nnjWDWorPL64o.txt', TemplateView.as_view(template_name='MP_verify_h59nnjWDWorPL64o.txt', content_type='text/plain')),
    re_path(r'^$', generic.RedirectView.as_view(
        url='/workflow/', permanent=False)),
    # re_path(r'', include(frontend_urls)),
    re_path(r'^$', generic.RedirectView.as_view(url='/workflow/', permanent=False)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
