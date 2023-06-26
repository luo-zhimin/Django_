from captcha.fields import CaptchaField
from django import forms

from .models import UserProfile, EmailVerifyCode


class UserRegisterForm(forms.Form):
    # 自动校验
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少3位',
        'max_length': '密码最多20位',
    })
    # 验证码
    captcha = CaptchaField()


class UserLoginForm(forms.Form):
    # 自动校验
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少3位',
        'max_length': '密码最多20位',
    })


class UserForgetForm(forms.Form):
    # 自动校验
    email = forms.EmailField(required=True)
    # 验证码
    captcha = CaptchaField()


class UserResetForm(forms.Form):
    # 自动校验
    password = forms.CharField(required=True, min_length=3, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少3位',
        'max_length': '密码最多20位',
    })
    password1 = forms.CharField(required=True, min_length=3, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少3位',
        'max_length': '密码最多20位',
    })


class UserChangeImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'phone']


class UserChangeEmailForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']


class UserRestEmailForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyCode
        fields = ['email', 'code']
