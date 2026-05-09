from django.core.paginator import Paginator


def get_paginated_queryset(queryset, request, per_page=10):

    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    total_pages = paginator.num_pages
    total_items = paginator.count
    page_range = list(paginator.page_range)

    start_index = max(current_page - 3, 1)
    end_index = min(current_page + 2, total_pages + 1)
    page_range = page_range[start_index - 1 : end_index]

    return {
        "page_obj": page_obj,
        "page_range": page_range,
        "current_page": current_page,
        "total_pages": total_pages,
        "total_items": total_items,
        "per_page": per_page,
    }