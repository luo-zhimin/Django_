from django.http import JsonResponse

from .forms import UserAskForm, UserCommentForm
from .models import UserLoveInfo, UserCommentInfo


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


def user_love(request):
    love_id = request.GET.get('love_id', '')
    love_type = request.GET.get('love_type', '')
    if love_id and love_type:
        # id/type 存在 去查找有没有这个机构
        print('user_love~~')
        love_list = UserLoveInfo.objects.filter(love_id=int(love_id), love_type=int(love_type), love_man=request.user)
        if love_list:
            # 现在是true 取消
            if love_list[0].love_status:
                love_list[0].love_status = False
                love_list[0].save()
                return JsonResponse({'status': 200, 'msg': '收藏'})
            else:
                # 现在是false 收藏
                love_list[0].love_status = True
                love_list[0].save()
                return JsonResponse({'status': 200, 'msg': '取消收藏'})
        else:
            # 不存在
            user_love_info = UserLoveInfo()
            user_love_info.love_man = request.user
            user_love_info.love_status = True
            user_love_info.love_id = int(love_id)
            user_love_info.love_type = int(love_type)
            user_love_info.save()
            return JsonResponse({'status': 200, 'msg': '取消收藏'})
    else:
        return JsonResponse({'status': 500, 'msg': '参数异常'})


def user_comment(request):
    user_comment_form = UserCommentForm(request.POST)
    if user_comment_form.is_valid():
        user_comment_info = UserCommentInfo()
        user_comment_info.comment_course_id = user_comment_form.cleaned_data['comment_course']
        user_comment_info.comment_content = user_comment_form.cleaned_data['comment_content']
        user_comment_info.comment_man = request.user
        user_comment_info.save()
        return JsonResponse({'status': 200, 'msg': '评论成功'})
    else:
        return JsonResponse({'status': 500, 'msg': '评论失败'})
