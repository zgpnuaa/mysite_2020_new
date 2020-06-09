from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 用户登录类型
type = (
    ('1', 'github'),
    ('2', 'qq'),
    ('3', 'weibo'),
)

class OAuth_ex(models.Model):
    user = models.ForeignKey(User, related_name='oauth_user', on_delete=models.CASCADE)
    openid = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=1, choices=type)

