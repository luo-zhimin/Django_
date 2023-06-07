from django.shortcuts import render

from orgs.views import get_love_status
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
        return render(request, 'courses/course-detail.html', {
            'course': course,
            'course_love_status': course_love_status,
            'org_love_status': org_love_status
        })
