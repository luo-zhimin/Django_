from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from .models import OrgInfo, CityInfo


# Create your views here.
def org_list(request):
    all_orgs = OrgInfo.objects.all()
    all_cites = CityInfo.objects.all()
    # 倒叙 切分3
    sort_orgs = all_orgs.order_by('-love_num')[:3]

    # 分页
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_orgs, 3)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'org-list.html', {
        'all_orgs': all_orgs,
        'pages': pages,
        'all_cites': all_cites,
        'sort_orgs': sort_orgs
    })
