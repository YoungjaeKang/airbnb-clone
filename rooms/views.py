from django.shortcuts import render


# from datetime import datetime
# from django.http import HttpResponse


def all_rooms(request):
    return render(request, "all_rooms")


""" 이게 아주 기본적인 형태이다.
    now = datetime.now()
    return HttpResponse(content=f"<h1>{now}</h1>") """

