from django.shortcuts import render
from . import get_requests
import colorama
from bs4 import UnicodeDammit
from django.http import HttpResponse

# Create your views here.
colorama.init(autoreset=True)

def index(request):
    return render(request, 'get/base.html', {})

def get(request, website):
    import urllib.parse
    decoded_website = urllib.parse.unquote(website)

    print(f"{colorama.Fore.GREEN}Fetching URL: {decoded_website}")
    try:

        URL = get_requests.get(decoded_website)
        
        import os
        os.makedirs("get/templates/get/project", exist_ok=True)
        with open("get/templates/get/project/index.html",
                  "w",
                   encoding=UnicodeDammit(URL.text).original_encoding) as f:
            print(f"{colorama.Fore.GREEN}Encoding: {UnicodeDammit(URL.text).original_encoding}")
            f.write(URL.text)
        return HttpResponse(URL.text)
    except Exception as e:
        print(f"{colorama.Fore.RED}Error fetching URL: {e}")
        raise