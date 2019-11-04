from django.urls import path
from rooms import views as room_views

# app_name이랑 urls.py config의 namespace랑 같아야 한다.
app_name = "core"

urlpatterns = [path("", room_views.all_rooms, name="home")]
