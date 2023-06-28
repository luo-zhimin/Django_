from operations.models import UserLoveInfo, UserMessageInfo


def get_love_status(request, love_id, love_type=1):
    """
    :param request: httpRequest
    :param love_id: 收藏id
    :param love_type: 收藏类型
    :return: 是否收藏
    """
    if request.user.is_authenticated:
        print('get_love_status~~~')
        love_list = UserLoveInfo.objects.filter(love_man=request.user, love_id=love_id, love_type=love_type)
        # todo !! 需要在这里 修改 org/course/teacher love_num
        # love_type 1 org 2 course 3 teacher
        if love_list:
            return love_list[0].love_status
        else:
            return False
    else:
        return False


def message_save(request, content):
    message = UserMessageInfo()
    message.message_content = content
    message.message_man = request.user.id
    message.save()
