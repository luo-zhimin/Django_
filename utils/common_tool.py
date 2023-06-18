from operations.models import UserLoveInfo
# from orgs.models import OrgInfo, TeacherInfo
# from courses.models import CourseInfo


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
            status = love_list[0].love_status
            # 需要判断请求 不然一刷新页面就当于一次新的请求
            # if love_type == 1:
            #     org = OrgInfo.objects.filter(id=int(love_id))[0]
            #     print(fr'org.love_num: {org.love_num}')
            #     org.love_num = org.love_num + handle_status(status)
            #     org.save()
            # elif love_type == 2:
            #     course = CourseInfo.objects.filter(id=int(love_id))[0]
            #     print(fr'course.love_num: {course.love_num}')
            #     course.love_num = course.love_num + handle_status(status)
            #     course.save()
            # else:
            #     teacher = TeacherInfo.objects.filter(id=int(love_id))[0]
            #     print(fr'teacher.love_num: {teacher.love_num}')
            #     teacher.love_num = teacher.love_num + handle_status(status)
            #     teacher.save()
            return status
        else:
            return False
    else:
        return False


def handle_status(status):
    if status:
        return 1
    else:
        return -1
