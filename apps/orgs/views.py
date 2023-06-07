from django.shortcuts import render

from operations.models import UserLoveInfo
from utils.page_tool import page
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

    pages = page(request,all_orgs)

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

        pages = page(request,all_course)

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
