from operations.models import UserLoveInfo


def get_love_status(request, love_id,love_type=1):
    """
    :param request: httpRequest
    :param love_id: 收藏id
    :param love_type: 收藏类型
    :return: 是否收藏
    """
    if request.user.is_authenticated:
        print('get_love_status~~~')
        love_list = UserLoveInfo.objects.filter(love_man=request.user, love_id=love_id, love_type=love_type)
        if love_list:
            return love_list[0].love_status
        else:
            return False
    else:
        return False