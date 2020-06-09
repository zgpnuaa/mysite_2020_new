from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, verbose_name='用户名')
    birth = models.DateField('生日', blank=True, null=True)
    phone = models.CharField('电话', max_length=20, null=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

    class Meta:
        verbose_name = '用户简况'
        verbose_name_plural = '用户简况'


class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, verbose_name='用户名')
    school = models.CharField('毕业院校', max_length=100, blank=True)
    company = models.CharField('工作单位', max_length=100, blank=True)
    profession = models.CharField('专业', max_length=100, blank=True)
    address = models.CharField('住址', max_length=100, blank=True)
    aboutme = models.TextField('自我介绍', blank=True)
    photo = models.ImageField('头像', upload_to='icons', blank=True)
    friends = models.ManyToManyField(User, related_name='my_friends', blank=True,  verbose_name='好友')

    def __str__(self):
        return "user:{}".format(self.user.username)

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            print('pppppp')
            return self.photo.url

    class Meta:
        verbose_name = '详细信息'
        verbose_name_plural = '详细信息'

