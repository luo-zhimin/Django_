from django.shortcuts import render

from operations.models import UserCourseInfo
from utils.common_tool import get_love_status
from utils.page_tool import page
from .models import CourseInfo


# Create your views here.
def course_list(request):
    all_courses = CourseInfo.objects.all()
    recommend_courses = all_courses.order_by('-add_time')[:3]

    sort = request.GET.get('sort', '')
    if sort:
        print(fr'-{sort}')
        all_courses = all_courses.order_by(fr'-{sort}')

    # 分页
    pages = page(request, all_courses)

    return render(request, 'courses/course-list.html', {
        'all_courses': all_courses,
        'recommend_courses': recommend_courses,
        'pages': pages,
        'sort': sort
    })


def course_detail(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        course_love_status = get_love_status(request, course_id, 2)
        org_love_status = get_love_status(request, course.org_info.id, 1)

        # 相关课程
        relate_courses = CourseInfo.objects.filter(category=course.category) \
                             .exclude(id=int(course_id))[:2]

        return render(request, 'courses/course-detail.html', {
            'course': course,
            'course_love_status': course_love_status,
            'org_love_status': org_love_status,
            'relate_courses': relate_courses
        })


def course_video(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        # 开始学习
        user_course_list = UserCourseInfo.objects.filter(study_man=request.user, study_course=course)
        if not user_course_list:
            user_course = UserCourseInfo()
            user_course.study_man = request.user
            user_course.study_course = course
            user_course.save()

        # 学过改课的同学还学过什么课程
        # same_courses = CourseInfo.objects.filter(category=course.category).exclude(id=int(course_id))[:2]
        user_course_list = UserCourseInfo.objects.filter(study_course=course)
        # 找到素有的用户的列表 列表生成式
        user_list = [u.study_man for u in user_course_list]
        user_course_list = UserCourseInfo.objects.filter(study_man__in=user_list) \
            .exclude(id=int(course_id))
        # 取课程去重
        course_list = list(set([c.study_course for c in user_course_list]))[:2]

        return render(request, 'courses/course-video.html', {
            'course': course,
            'course_list': course_list
        })
