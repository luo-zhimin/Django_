import re

from django import forms

from .models import UserAskInfo


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAskInfo
        # 排除
        # exclude=['add_time']
        # 全部
        # fields = ['__all__']
        fields = ['name', 'course', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # 正则
        co = re.compile('^1[3|4|5|6|7|8|9]\\d{9}$')
        if co.match(phone):
            return phone
        else:
            raise forms.ValidationError('手机号码不合法')

    # def clean_course(self):
    # 可以校验是否有该课程


# class UserCommentForm(forms.ModelForm):
#     class Meta:
#         model = UserCommentInfo
#         fields = ['comment_man', 'comment_course', 'comment_content']

class UserCommentForm(forms.Form):
    comment_course = forms.IntegerField(required=True)
    comment_content = forms.CharField(required=True, min_length=1, max_length=100)
