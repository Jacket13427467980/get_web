import os
from django.shortcuts import render
import colorama
from . import get_requests
from . import headle_URL

# Create your views here.
colorama.init(autoreset=True)

TEMPLATES = list()

def index(request):
    return render(request, 'get/base.html', {})

def append(template):
    TEMPLATES.append(template)

def get(request, website):
    import urllib.parse
    decoded_website = urllib.parse.unquote(website)

    print(f"{colorama.Fore.GREEN}Fetching URL: {decoded_website}")
    try:

        request = get_requests.get(decoded_website)

        headle_url = headle_URL.multiple_requests(request.url)
        for url in headle_url(request.text):
            file_path = f"get/templates/get/project/{url}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
            except Exception as e:
                print(f"{colorama.Fore.RED}Error matched URL: {url} Error: {e}")
            with open(file_path, "w", encoding=request.encoding) as f:
                try:
                    f.write(request.text)
                except Exception as e:
                    print(f"{colorama.Fore.RED}Error writed to file\tfile_name: {f.name} Error: {e}")
                else:
                    print(f"{colorama.Fore.GREEN}Correctly matched URL: {url}\nWrited to file: {f.name}")
        print(headle_url)
        return render(request, "get/base.html", {})
    except Exception as e:
        print(f"{colorama.Fore.RED}Catched an error: {e}")
        raise