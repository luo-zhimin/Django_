from django.shortcuts import render

from .models import OrgInfo, CityInfo


# Create your views here.
def org_list(request):
    all_orgs = OrgInfo.objects.all()
    all_cites = CityInfo.objects.all()

    sort_orgs = all_orgs.order_by('-love_num')[:3]

    return render(request, 'org-list.html', {
        'all_orgs': all_orgs,
        'all_cites': all_cites,
        'sort_orgs': sort_orgs
    })
