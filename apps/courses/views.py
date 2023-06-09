from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View

from operations.models import UserCommentInfo
from operations.models import UserCourseInfo
from utils.common_tool import get_love_status
# from django.contrib.auth.decorators import login_required
from utils.decorators import login_decorators
from utils.page_tool import page
from .models import CourseInfo


# Create your views here.
class CourseListView(View):
    def get(self, request):
        all_courses = CourseInfo.objects.all()
        recommend_courses = all_courses.order_by('-add_time')[:3]

        sort = request.GET.get('sort', '')
        if sort:
            print(fr'-{sort}')
            all_courses = all_courses.order_by(fr'-{sort}')

        keyword = request.GET.get('keyword', '')
        if keyword:
            all_courses = all_courses.filter(
                Q(name__icontains=keyword) | Q(desc__icontains=keyword) | Q(detail__icontains=keyword))
        # 分页
        pages = page(request, all_courses)

        return render(request, 'courses/course-list.html', {
            'all_courses': all_courses,
            'recommend_courses': recommend_courses,
            'pages': pages,
            'sort': sort,
            'keyword': keyword
        })


# def course_list(request):
#     all_courses = CourseInfo.objects.all()
#     recommend_courses = all_courses.order_by('-add_time')[:3]
#
#     sort = request.GET.get('sort', '')
#     if sort:
#         print(fr'-{sort}')
#         all_courses = all_courses.order_by(fr'-{sort}')
#
#     keyword = request.GET.get('keyword', '')
#     if keyword:
#         all_courses = all_courses.filter(
#             Q(name__icontains=keyword) | Q(desc__icontains=keyword) | Q(detail__icontains=keyword))
#     # 分页
#     pages = page(request, all_courses)
#
#     return render(request, 'courses/course-list.html', {
#         'all_courses': all_courses,
#         'recommend_courses': recommend_courses,
#         'pages': pages,
#         'sort': sort,
#         'keyword': keyword
#     })


class CourseDetailView(View):
    def get(self, request, course_id):
        print(fr"course_detail:{course_id}")
        if course_id:
            course = CourseInfo.objects.filter(id=int(course_id))[0]
            course.click_num += 1
            course.save()

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


# def course_detail(request, course_id):
#     print(fr"course_detail:{course_id}")
#     if course_id:
#         course = CourseInfo.objects.filter(id=int(course_id))[0]
#         course.click_num += 1
#         course.save()
#
#         course_love_status = get_love_status(request, course_id, 2)
#         org_love_status = get_love_status(request, course.org_info.id, 1)
#
#         # 相关课程
#         relate_courses = CourseInfo.objects.filter(category=course.category) \
#                              .exclude(id=int(course_id))[:2]
#
#         return render(request, 'courses/course-detail.html', {
#             'course': course,
#             'course_love_status': course_love_status,
#             'org_love_status': org_love_status,
#             'relate_courses': relate_courses
#         })

class CourseVideoView(View):
    @login_decorators
    def get(self, request, course_id):
        if course_id:
            course = CourseInfo.objects.filter(id=int(course_id))[0]
            # 开始学习
            user_course_list = UserCourseInfo.objects.filter(study_man=request.user, study_course=course)
            if not user_course_list:
                user_course = UserCourseInfo()
                user_course.study_man = request.user
                user_course.study_course = course
                user_course.save()
                # 第一次学习 时候加+1 课程
                course.study_num += 1
                course.save()
                course.org_info.study_num += 1
                course.org_info.save()

            return render(request, 'courses/course-video.html', {
                'course': course,
                'course_list': get_study_course_list(course)
            })


# @login_required(login_url='/users/user_login')
# @login_decorators
# def course_video(request, course_id):
#     if course_id:
#         course = CourseInfo.objects.filter(id=int(course_id))[0]
#         # 开始学习
#         user_course_list = UserCourseInfo.objects.filter(study_man=request.user, study_course=course)
#         if not user_course_list:
#             user_course = UserCourseInfo()
#             user_course.study_man = request.user
#             user_course.study_course = course
#             user_course.save()
#             # 第一次学习 时候加+1 课程
#             course.study_num += 1
#             course.save()
#             course.org_info.study_num += 1
#             course.org_info.save()
#
#         return render(request, 'courses/course-video.html', {
#             'course': course,
#             'course_list': get_study_course_list(course)
#         })

class CourseCommentView(View):
    def get(self, request, course_id):
        if course_id:
            course = CourseInfo.objects.filter(id=int(course_id))[0]
            user_comment_course_list = UserCommentInfo.objects.filter(comment_course_id=course.id)[:10]
            return render(request, 'courses/course-comment.html', {
                'course': course,
                'course_list': get_study_course_list(course),
                'user_comment_course_list': user_comment_course_list
            })


# def course_comment(request, course_id):
#     if course_id:
#         course = CourseInfo.objects.filter(id=int(course_id))[0]
#         user_comment_course_list = UserCommentInfo.objects.filter(comment_course_id=course.id)[:10]
#         return render(request, 'courses/course-comment.html', {
#             'course': course,
#             'course_list': get_study_course_list(course),
#             'user_comment_course_list': user_comment_course_list
#         })


def get_study_course_list(course):
    # 学过改课的同学还学过什么课程
    user_course_list = UserCourseInfo.objects.filter(study_course=course)
    # 找到素有的用户的列表 列表生成式
    user_list = [u.study_man for u in user_course_list]
    user_course_list = UserCourseInfo.objects.filter(study_man__in=user_list) \
        .exclude(id=int(course.id))
    # 取课程去重
    return list(set([c.study_course for c in user_course_list]))[:2]
