from django.shortcuts import render

from utils.common_tool import get_love_status
from utils.page_tool import page
from .models import OrgInfo, CityInfo, TeacherInfo


# Create your views here.
def org_list(request):
    all_orgs = OrgInfo.objects.all()
    all_cites = CityInfo.objects.all()
    # 倒叙 切分3
    sort_orgs = all_orgs.order_by('-love_num')[:3]
    # 按照机构类别进行过滤
    category = request.GET.get('category', '')
    if category:
        all_orgs = all_orgs.filter(category=category)
    city_id = request.GET.get('city_id', '')
    if city_id:
        all_orgs = all_orgs.filter(city_info_id=city_id)

    # 排序
    sort = request.GET.get('sort', '')
    if sort:
        # print(fr'-{sort}')
        # todo 重新赋值
        all_orgs = all_orgs.order_by(fr'-{sort}')

    pages = page(request, all_orgs)

    return render(request, 'orgs/org-list.html', {
        'all_orgs': all_orgs,
        'pages': pages,
        'all_cites': all_cites,
        'sort_orgs': sort_orgs,
        'category': category,
        'city_id': city_id,
        'sort': sort
    })


def org_detail(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        love_status = get_love_status(request, org_id)

        return render(request, 'orgs/org-detail-homepage.html', {
            'org': org,
            'love_status': love_status
        })


def org_detail_course(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]

        all_course = org.courseinfo_set.all()

        pages = page(request, all_course)

        love_status = get_love_status(request, org_id)

        return render(request, 'orgs/org-detail-course.html', {
            'org': org,
            'pages': pages,
            'love_status': love_status
        })


def org_detail_desc(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        love_status = get_love_status(request, org_id)
        return render(request, 'orgs/org-detail-desc.html', {
            'org': org,
            'love_status': love_status
        })


def org_detail_teachers(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        love_status = get_love_status(request, org_id)
        return render(request, 'orgs/org-detail-teachers.html', {
            'org': org,
            'love_status': love_status
        })


def teacher_list(request):
    teachers = TeacherInfo.objects.all()
    sort_teachers = teachers.order_by('-love_num')[:3]

    # 排序
    sort = request.GET.get('sort', '')
    if sort:
        # print(fr'-{sort}')
        teachers = teachers.order_by(fr'-{sort}')

    pages = page(request, teachers)
    return render(request, 'orgs/teachers-list.html', {
        'teachers': teachers,
        'sort_teachers': sort_teachers,
        'pages': pages,
        'sort': sort
    })


def teacher_detail(request, teacher_id):
    if teacher_id:
        teacher = TeacherInfo.objects.filter(id=int(teacher_id))[0]
        teachers = TeacherInfo.objects.all()
        sort_teachers = teachers.order_by('-love_num')[:3]
        love_status = get_love_status(request, teacher.work_company.id)
        love_teacher_status = get_love_status(request, teacher.id)
        return render(request, 'orgs/teacher-detail.html', {
            'teacher': teacher,
            'sort_teachers': sort_teachers,
            'love_status': love_status,
            'love_teacher_status': love_teacher_status,
        })
