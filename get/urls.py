from django.urls import path
from . import views

app_name = "get"

urlpatterns = [
    path("", views.index, name="index"),
    path("get/<path:_website>/", views.get, name="get"),
    path("api/get/<path:url>/", views.get_response, name="get_response")
]    