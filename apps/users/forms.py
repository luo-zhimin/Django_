from django import forms


class UserRegisterForm(forms.Form):
    # 自动校验
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少3位',
        'max_length': '密码最多20位',
    })
