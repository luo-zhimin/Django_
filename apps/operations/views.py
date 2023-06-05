from django.http import JsonResponse

from .forms import UserAskForm


# Create your views here.

def user_ask(request):
    user_ask_form = UserAskForm(request.POST)
    if user_ask_form.is_valid():
        # name = user_ask_form.cleaned_data['name']
        # 自动提交
        user_ask_form.save(commit=True)
        return JsonResponse({'status': 200, 'msg': '咨询成功'})
    else:
        return JsonResponse({'status': 500, 'msg': '咨询失败'})
