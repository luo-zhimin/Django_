# 装饰器 闭包 外部调用内部
# MQ(3) ES KAFKA
from django.http.response import JsonResponse
from django.shortcuts import reverse, redirect


def login_decorators(fun):
    def inner(request, *args, **kwargs):
        # print(request.user.is_authenticated)
        # if request.user.is_authenticated:
        # View -> request.request
        if request.request.user.is_authenticated:
            print(22)
            return fun(request, *args, **kwargs)
        else:
            # ajax
            # print(request.is_ajax)
            # if request.is_ajax():
            url = request.request.get_full_path()
            print('login_decorators-> ', url)
            if request.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # return JsonResponse({'status', 403})
                return JsonResponse({'status': 403})

            # 不考虑从哪里来回哪里去 第一层
            ret = redirect(reverse('users:user_login'))
            # 从哪里来回哪里去
            ret.set_cookie('url', url)
            return ret

    return inner
