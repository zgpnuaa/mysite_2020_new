from django.db import models

# Create your models here.


class CpuInfo(models.Model):
    # CPU信息
    time = models.DateTimeField()
    host = models.CharField(max_length=40)
    usage_system = models.FloatField(null=True)
    usage_user = models.FloatField(null=True)
    usage_softirq = models.FloatField(null=True)
    usage_iowait = models.FloatField(null=True)


class MemoryInfo(models.Model):
    #内存信息
    time = models.DateTimeField()
    host = models.CharField(max_length=40)
    used_percent = models.FloatField(null=True)


class ProcstatInfo(models.Model):
    # 进程信息
    time = models.DateTimeField()
    host = models.CharField(max_length=100)
    exe = models.CharField(max_length=40)
    pid = models.FloatField()
    cpu_usage = models.FloatField(null=True)
    memory_rss = models.FloatField(null=True)

