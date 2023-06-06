from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from .models import OrgInfo, CityInfo


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

    # 分页
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_orgs, 3)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

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
        return render(request, 'orgs/org-detail-homepage.html', {
            'org': org
        })


def org_detail_course(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]

        all_course = org.courseinfo_set.all()
        page_num = request.GET.get('page_num', '')
        pa = Paginator(all_course, 3)
        try:
            pages = pa.page(page_num)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)

        return render(request, 'orgs/org-detail-course.html', {
            'org': org,
            'pages': pages
        })


def org_detail_desc(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        return render(request, 'orgs/org-detail-desc.html', {
            'org': org
        })


def org_detail_teachers(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        return render(request, 'orgs/org-detail-teachers.html', {
            'org': org
        })
