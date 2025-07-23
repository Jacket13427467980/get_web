from django.urls import path
from . import views

app_name = "get"

urlpatterns = [
    path("", views.index, name="index"),
    path("get/<path:website>/", views.get, name="get"),
]
