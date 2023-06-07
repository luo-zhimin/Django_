from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def page(request, data_list, number=3):
    """
    :param request: httpRequest
    :param data_list: 要进行分页的数据
    :param number: 每页的数量 默认3
    :return: 分页好的数据
    """
    # 分页
    page_num = request.GET.get('pagenum', '')
    pa = Paginator(data_list, number)
    try:
        return pa.page(page_num)
    except PageNotAnInteger:
        return pa.page(1)
    except EmptyPage:
        return pa.page(pa.num_pages)
