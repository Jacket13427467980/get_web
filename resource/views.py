from django.shortcuts import render
from get import get_requests


# Create your views here.

def resource(request, resource_id):
    response = get_requests.get(f"http://{request.get_host()}/resource/{resource_id}")
    return render(request, "resource/resource.html", {"response": response})