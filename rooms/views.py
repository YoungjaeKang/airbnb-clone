# from math import ceil
from django.views.generic import ListView, DetailView, View
from django.http import Http404
from django_countries import countries
from django.core.paginator import Paginator

# from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django.shortcuts import render, redirect
from . import models
from . import forms


# class based view와 function based view 사이에 논쟁이 많다.
class HomeView(ListView):

    """ HomeView Definition """

    # ccbv
    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


# 1. cbv
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room
    # 다양한 attribute를 통해 통제할 수 있다.
    # 404도 자동으로 띄워준다.


class SearchView(View):
    """ SearchView Definition """

    def get(self, request):
        country = request.GET.get("country")

        # http://127.0.0.1:8000/rooms/search/ 로 들어갔을 때 빈 값에 대한 default를 주기 위한 코드
        if country:
            
            form = forms.SearchForm(request.GET)    # request.GET으로 form은 입력한 검색 값을 기억한다.
            
            if form.is_valid():

                # print(form.cleaned_data)

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                # filter =================================
                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

        else:
            
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


# 2. fbv
def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})

    except models.Room.DoesNotExist:
        # return redirect(reverse("core:home"))
        raise Http404()  # error는 return이 아니라 raise한다


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

