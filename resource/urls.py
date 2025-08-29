from django.urls import path
from . import views

app_name = "resource"

urlpatterns = [
    path("<int:resource_id>", views.resource, name="resource")
]