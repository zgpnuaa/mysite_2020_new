from django.contrib import admin
from .models import UserProfile, UserInfo, User


# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    # 设置要展示的模型字段，作为表头
    list_display = ('user', 'birth', 'phone')
    # 设置过滤器，并在页面右侧生成导航栏，若有外键，应使用双下划线连接两个模型的字段
    list_filter = ('user__username', 'phone',)
    # 设置搜索字段，若有外键，应使用双下划线连接两个模型的字段
    search_fields = ('user__username',  'phone',)  # 这里user字段与外表的User的username一对一关系，需用双下划线连接两个模型的字段
    # 设置排序方式
    ordering = ['id']
    # 设置时间选择器,字段中有时间格式才能使用
    # date_hierarchy = Field
    # 设置编辑和添加的数据字段
    fields = ['user',  'birth', 'phone', ]
    # 设置只读字段
    readonly_fields = ['user']



admin.site.register(UserProfile, UserProfileAdmin)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'company', 'profession', 'address', 'aboutme', 'photo')
    list_filter = ('school', 'company', 'profession')
    search_fields = ('user__username', 'school', 'company', 'profession', 'address', 'aboutme',)
    readonly_fields = ['user']

admin.site.register(UserInfo, UserInfoAdmin)


admin.site.site_title = '流花岛后台管理'
admin.site.site_header = '“流花岛”后台管理系统'


