from math import ceil
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models

# from datetime import datetime
# from django.http import HttpResponse


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    rooms = paginator.page(int(page))
    return render(request, "rooms/home.html", {"page": rooms})

    """
    1. 수동으로 페이지네이션을 구현하는 방법
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)

    return render(
        request,
        "rooms/home.html",
        context={
            "potato": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count),
        },
    )
    """


""" 이게 아주 기본적인 형태이다.
    now = datetime.now()
    return HttpResponse(content=f"<h1>{now}</h1>") """

