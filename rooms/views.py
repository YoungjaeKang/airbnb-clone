# from math import ceil
from django.views.generic import ListView, DetailView
from django.http import Http404

# from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django.shortcuts import render, redirect
from . import models

# class based view와 function based view 사이에 논쟁이 많다.
class HomeView(ListView):

    """ HomeView Definition """

    # ccbv
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


# 1. cbv
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room
    # 다양한 attribute를 통해 통제할 수 있다.
    # 404도 자동으로 띄워준다.


"""
# 2. fbv
def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})

    except models.Room.DoesNotExist:
        # return redirect(reverse("core:home"))
        raise Http404()  # error는 return이 아니라 raise한다
"""

"""
2. Django의 도움을 조금만 받기
def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)

    # 없는 페이지의 url을 넣었을 때 home으로 돌려보내고 url을 정상적으로 보이게 한다.
    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")"""

""" 1. 수동으로 페이지네이션을 구현하는 방법
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

