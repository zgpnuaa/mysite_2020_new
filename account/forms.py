from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo
from django.core import validators


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'onblur':'check_username(this.value)', 'oninvalid': 'setCustomValidity("请输入用户名")', 'oninput': 'setCustomValidity("")'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'onblur':'check_email(this.value)',  'oninvalid': 'setCustomValidity("请输入邮箱")', 'oninput': 'setCustomValidity("")'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'onblur': 'check_password1(this.value)',  'oninvalid': 'setCustomValidity("请输入密码")', 'oninput': 'setCustomValidity("")'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'onblur': 'check_password2(this.value)',  'oninvalid': 'setCustomValidity("请再次输入密码")', 'oninput': 'setCustomValidity("")'}))

    class Meta:
        model = User
        fields = ("username", "email",)

    # "clean_+属性名称的方法，会在调用实例对象的is_valid()方法时被执行"
    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError("两次密码输入不相同！")
    #     return cd['password2']


class UserProfileForm(forms.ModelForm):
    birth = forms.DateField(widget=forms.DateInput(attrs={'onblur': 'check_birthday(this.value)',  'oninvalid': 'setCustomValidity("请输入生日")', 'oninput': 'setCustomValidity("")'}))
    phone = forms.CharField(validators=[validators.RegexValidator(regex=r"^1[3-9]\d{9}$", message="手机号码格式不正确")], widget=forms.DateInput(attrs={'onblur': 'check_phone(this.value)',  'oninvalid': 'setCustomValidity("请输入手机号码")', 'oninput': 'setCustomValidity("")'}), error_messages={"min_length": "手机号长度有误", "max_length": "手机号长度有误",
                                             "required": "手机号不能为空"})

    class Meta:
        model = UserProfile
        fields = ("phone", "birth")


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme", "photo")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)


