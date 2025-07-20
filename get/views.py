from django.shortcuts import render
from . import get_requests
import colorama
from django.http import HttpResponse
from pathlib import Path

# Create your views here.
colorama.init(autoreset=True)

def index(request):
    return render(request, 'get/base.html', {})

def get(request, website):
    print(f"{colorama.Fore.GREEN}Fetching URL: {website}")
    URL = get_requests.get(website)
    open("C:\\Users\\琳琳\\Desktop\\刘梓祺\\作品\\get\\get\\templates\\get\\project", "w").write(URL.text)
    return HttpResponse(URL.text)