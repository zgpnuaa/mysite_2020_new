from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AstrologyInfo(models.Model):
    user = models.ForeignKey(User, related_name="astrology", blank=True, null=True, on_delete=models.SET_NULL, verbose_name='用户')
    latitude = models.CharField('纬度', max_length=30, null=False)
    longitude = models.CharField('经度', max_length=30, null=False)
    date = models.CharField('日期', max_length=30, null=False)
    time = models.CharField('时间', max_length=30, null=False)
    accuracy = models.CharField('准确度反馈', max_length=30, null=True)
    feedback = models.TextField('意见反馈', null=True)

    class Meta:
        verbose_name = '个人星座信息'
        verbose_name_plural = '个人星座信息'

class ConstellationIntroduction(models.Model):
    constellation = models.CharField('星座', max_length=30, null=False)
    introduction = models.TextField('介绍', null=False)

    class Meta:
        verbose_name = '星座介绍'
        verbose_name_plural = '星座介绍'


class PlanetIntroduction(models.Model):
    planet = models.CharField('行星', max_length=30, null=False)
    introduction = models.TextField('介绍', null=False)

    class Meta:
        verbose_name = '行星介绍'
        verbose_name_plural = '行星介绍'


class HouseIntroduction(models.Model):
    house = models.CharField('宫位', max_length=30, null=False)
    introduction = models.TextField('介绍', null=False)

    class Meta:
        verbose_name = '宫位介绍'
        verbose_name_plural = '宫位介绍'


class AnglesIntroduction(models.Model):
    angle = models.CharField('基本点', max_length=30, null=False)
    introduction = models.TextField('介绍', null=False)

    class Meta:
        verbose_name = '基本点介绍'
        verbose_name_plural = '基本点介绍'


class NodeIntroduction(models.Model):
    node = models.CharField('月亮南北交点', max_length=30, null=False)
    introduction = models.TextField('介绍', null=False)

    class Meta:
        verbose_name = '月亮南北交点介绍'
        verbose_name_plural = '月亮南北交点介绍'


class SunSign(models.Model):
    sign = models.CharField('太阳星座', max_length=30, null=False)
    meaning = models.TextField('太阳星座解读')
    house_meaning = models.TextField('太阳宫位解读', default="")

    class Meta:
        verbose_name = '太阳星座'
        verbose_name_plural = '太阳星座'


class MOONSign(models.Model):
    sign = models.CharField('月亮星座', max_length=30, null=False)
    meaning = models.TextField('月亮星座解读')
    house_meaning = models.TextField('月亮宫位解读', default="")

    class Meta:
        verbose_name = '月亮星座'
        verbose_name_plural = '月亮星座'


class MERCURYSign(models.Model):
    sign = models.CharField('水星星座', max_length=30, null=False)
    meaning = models.TextField('水星星座解读')
    house_meaning = models.TextField('水星宫位解读', default="")

    class Meta:
        verbose_name = '水星星座'
        verbose_name_plural = '水星星座'


class VENUSSign(models.Model):
    sign = models.CharField('金星星座', max_length=30, null=False)
    meaning = models.TextField('金星星座解读')
    house_meaning = models.TextField('金星宫位解读', default="")

    class Meta:
        verbose_name = '金星星座'
        verbose_name_plural = '金星星座'


class MARSSign(models.Model):
    sign = models.CharField('火星星座', max_length=30, null=False)
    meaning = models.TextField('火星星座解读')
    house_meaning = models.TextField('火星宫位解读', default="")

    class Meta:
        verbose_name = '火星星座'
        verbose_name_plural = '火星星座'


class JUPITERSign(models.Model):
    sign = models.CharField('木星星座', max_length=30, null=False)
    meaning = models.TextField('木星星座解读')
    house_meaning = models.TextField('木星宫位解读', default="")

    class Meta:
        verbose_name = '木星星座'
        verbose_name_plural = '木星星座'


class SATURNSign(models.Model):
    sign = models.CharField('土星星座', max_length=30, null=False)
    meaning = models.TextField('土星星座解读')
    house_meaning = models.TextField('土星宫位解读', default="")

    class Meta:
        verbose_name = '土星星座'
        verbose_name_plural = '土星星座'


class URANUSSign(models.Model):
    sign = models.CharField('天王星星座', max_length=30, null=False)
    meaning = models.TextField('天王星星座解读')
    house_meaning = models.TextField('天王星宫位解读', default="")

    class Meta:
        verbose_name = '天王星星座'
        verbose_name_plural = '天王星星座'


class NEPTUNESign(models.Model):
    sign = models.CharField('海王星星座', max_length=30, null=False)
    meaning = models.TextField('海王星星座解读')
    house_meaning = models.TextField('海王星宫位解读', default="")

    class Meta:
        verbose_name = '海王星星座'
        verbose_name_plural = '海王星星座'


class PLUTOSign(models.Model):
    sign = models.CharField('冥王星星座', max_length=30, null=False)
    meaning = models.TextField('冥王星星座解读')
    house_meaning = models.TextField('冥王星宫位解读', default="")

    class Meta:
        verbose_name = '冥王星星座'
        verbose_name_plural = '冥王星星座'


class CHIRONSign(models.Model):
    sign = models.CharField('凯龙星星座', max_length=30, null=False)
    house_meaning = models.TextField('太阳宫位解读', default="")
    meaning = models.TextField('凯龙星星座解读')

    class Meta:
        verbose_name = '凯龙星星座'
        verbose_name_plural = '凯龙星星座'


class AscSign(models.Model):
    sign = models.CharField('上升星座', max_length=30, null=False)
    meaning = models.TextField('上升星座解读')

    class Meta:
        verbose_name = '上升星座'
        verbose_name_plural = '上升星座'


class DesSign(models.Model):
    sign = models.CharField('下降星座', max_length=30, null=False)
    meaning = models.TextField('下降星座解读')

    class Meta:
        verbose_name = '下降星座'
        verbose_name_plural = '下降星座'


class MCSign(models.Model):
    sign = models.CharField('天顶星座', max_length=30, null=False)
    meaning = models.TextField('天顶星座解读')

    class Meta:
        verbose_name = '天顶星座'
        verbose_name_plural = '天顶星座'


class ICSign(models.Model):
    sign = models.CharField('天底星座', max_length=30, null=False)
    meaning = models.TextField('天底星座解读')

    class Meta:
        verbose_name = '天底星座'
        verbose_name_plural = '天底星座'


class NNodeSign(models.Model):
    sign = models.CharField('北交点星座', max_length=30, null=False)
    meaning = models.TextField('北交点星座解读')

    class Meta:
        verbose_name = '北交点星座'
        verbose_name_plural = '北交点星座'


class SNodeSign(models.Model):
    sign = models.CharField('南交点星座', max_length=30, null=False)
    meaning = models.TextField('南交点星座解读')

    class Meta:
        verbose_name = '南交点星座'
        verbose_name_plural = '南交点星座'


class HOUSE1(models.Model):
    sign = models.CharField('第一宫星座', max_length=30, null=False)
    meaning = models.TextField('第一宫星座解读')

    class Meta:
        verbose_name = '第一宫星座'
        verbose_name_plural = '第一宫星座'


class HOUSE2(models.Model):
    sign = models.CharField('第二宫星座', max_length=30, null=False)
    meaning = models.TextField('第二宫星座解读')

    class Meta:
        verbose_name = '第二宫星座'
        verbose_name_plural = '第二宫星座'


class HOUSE3(models.Model):
    sign = models.CharField('第三宫星座', max_length=30, null=False)
    meaning = models.TextField('第三宫星座解读')

    class Meta:
        verbose_name = '第三宫星座'
        verbose_name_plural = '第三宫星座'


class HOUSE4(models.Model):
    sign = models.CharField('第四宫宫座', max_length=30, null=False)
    meaning = models.TextField('第四宫星座解读')

    class Meta:
        verbose_name = '第四宫星座'
        verbose_name_plural = '第四宫星座'


class HOUSE5(models.Model):
    sign = models.CharField('第五宫星座', max_length=30, null=False)
    meaning = models.TextField('第五宫星座解读')

    class Meta:
        verbose_name = '第五宫星座'
        verbose_name_plural = '第五宫星座'


class HOUSE6(models.Model):
    sign = models.CharField('第六宫星座', max_length=30, null=False)
    meaning = models.TextField('第六宫星座解读')

    class Meta:
        verbose_name = '第六宫星座'
        verbose_name_plural = '第六宫星座'


class HOUSE7(models.Model):
    sign = models.CharField('第七宫星座', max_length=30, null=False)
    meaning = models.TextField('第七宫星座解读')

    class Meta:
        verbose_name = '第七宫星座'
        verbose_name_plural = '第七宫星座'


class HOUSE8(models.Model):
    sign = models.CharField('第八宫星座', max_length=30, null=False)
    meaning = models.TextField('第八宫星座解读')

    class Meta:
        verbose_name = '第八宫星座'
        verbose_name_plural = '第八宫星座'


class HOUSE9(models.Model):
    sign = models.CharField('第九宫星座', max_length=30, null=False)
    meaning = models.TextField('第九宫星座解读')

    class Meta:
        verbose_name = '第九宫星座'
        verbose_name_plural = '第九宫星座'


class HOUSE10(models.Model):
    sign = models.CharField('第十宫星座', max_length=30, null=False)
    meaning = models.TextField('第十宫星座解读')

    class Meta:
        verbose_name = '第十宫星座'
        verbose_name_plural = '第十宫星座'


class HOUSE11(models.Model):
    sign = models.CharField('第十一宫星座', max_length=30, null=False)
    meaning = models.TextField('第十一宫星座解读')

    class Meta:
        verbose_name = '第十一宫星座'
        verbose_name_plural = '第十一宫星座'


class HOUSE12(models.Model):
    sign = models.CharField('第十二宫星座', max_length=30, null=False)
    meaning = models.TextField('第十二宫星座解读')

    class Meta:
        verbose_name = '第十二宫星座'
        verbose_name_plural = '第十二宫星座'

