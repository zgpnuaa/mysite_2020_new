from django.db import models
import django.utils.timezone as timezone


# Create your models here.


class WxToken(models.Model):
    token = models.CharField(max_length=200)
    lifetime = models.DateTimeField(
        default=0
    )

    def get_date(self):
        delta = timezone.now() - self.lifetime
        if delta.seconds < 6000:
            return True
        else:
            return False


class JsToken(models.Model):
    token = models.CharField(max_length=200)
    lifetime = models.DateTimeField(
        default=0
    )

    def get_date(self):
        delta = timezone.now() - self.lifetime
        if delta.seconds < 6000:
            return True
        else:
            return False