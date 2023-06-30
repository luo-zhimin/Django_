from django.http import JsonResponse

from courses.models import CourseInfo
from orgs.models import OrgInfo, TeacherInfo
from utils.decorators import login_decorators
from .forms import UserAskForm, UserCommentForm
from .models import UserLoveInfo, UserCommentInfo, UserMessageInfo


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


@login_decorators
def user_love(request):
    love_id = request.GET.get('love_id', '')
    love_type = request.GET.get('love_type', '')
    if love_id and love_type:
        # 需要判断请求 不然一刷新页面就当于一次新的请求
        data = None
        if love_type == '1':
            data = OrgInfo.objects.filter(id=int(love_id))[0]
        elif love_type == '2':
            data = CourseInfo.objects.filter(id=int(love_id))[0]
        else:
            data = TeacherInfo.objects.filter(id=int(love_id))[0]

        # id/type 存在 去查找有没有这个机构
        print('user_love~~')
        love_list = UserLoveInfo.objects.filter(love_id=int(love_id), love_type=int(love_type), love_man=request.user)
        if love_list:
            # 现在是true 取消
            if love_list[0].love_status:
                love_list[0].love_status = False
                love_list[0].save()
                data.love_num -= 1
                data.save()
                return JsonResponse({'status': 200, 'msg': '收藏'})
            else:
                # 现在是false 收藏
                love_list[0].love_status = True
                love_list[0].save()
                data.love_num += 1
                data.save()
                return JsonResponse({'status': 200, 'msg': '取消收藏'})
        else:
            # 不存在
            user_love_info = UserLoveInfo()
            user_love_info.love_man = request.user
            user_love_info.love_status = True
            user_love_info.love_id = int(love_id)
            user_love_info.love_type = int(love_type)
            user_love_info.save()
            data.love_num += 1
            data.save()
            return JsonResponse({'status': 200, 'msg': '取消收藏'})
    else:
        return JsonResponse({'status': 500, 'msg': '参数异常'})


@login_decorators
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


@login_decorators
def user_delete_love(request):
    love_id = request.GET.get('love_id', '')
    love_type = request.GET.get('love_type', '')
    if love_id and love_type:
        user_love_info = \
            UserLoveInfo.objects.filter(love_type=int(love_type), love_id=int(love_id), love_man=request.user,
                                        love_status=True)[0]
        if user_love_info:
            user_love_info.love_status = False
            user_love_info.save()
            return JsonResponse({'status': 200, 'msg': '取消成功'})
        else:
            pass
    else:
        pass


@login_decorators
def user_message(request):
    message_id = request.GET.get('message_id', '')
    status = request.GET.get('status', '')
    if message_id and status:
        message = UserMessageInfo.objects.filter(id=int(message_id))[0]
        message.message_status = status
        message.save()
        return JsonResponse({'status': 200, 'msg': '消息已读'})
    else:
        pass
