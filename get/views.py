import os
from django.shortcuts import render
from . import get_requests
import colorama
from . import headle_URL

# Create your views here.
colorama.init(autoreset=True)

def index(request):
    try:
        if os.path.exists("get/templates/get/project/"):
            for file in os.listdir("get/templates/get/project"):
                os.remove(os.path.join("get/templates/get/project", file))
    except Exception as e:
        print(f"{colorama.Fore.RED}Error cleaning project directory: {e}")
    return render(request, 'get/base.html', {})

def get(request, website):
    import urllib.parse
    decoded_website = urllib.parse.unquote(website)

    print(f"{colorama.Fore.GREEN}Fetching URL: {decoded_website}")
    try:

        request = get_requests.get(decoded_website)
        
        os.makedirs("get/templates/get/project", exist_ok=True)
        with open("get/templates/get/project/index.html",
                  "w",
                   encoding=request.encoding) as f:
            print(f"{colorama.Fore.GREEN}Encoding: {request.encoding}")
            f.write(request.text)

        headle_url = headle_URL.headle_text(request.text, decoded_website)


        for i in headle_url:
            file_path = f"get/templates/get/project/{i}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            try:
                request = get_requests.get(i)
            except Exception as e:
                print(f"{colorama.Fore.RED}Error matched URL: {i} Error: {e}")
            with open(file_path, "w", encoding=request.encoding) as f:
                try:
                    f.write(request.text)
                except Exception as e:
                    print(f"{colorama.Fore.RED}Error writed to file\tfile_name: {f.name} Error: {e}")
                else:
                    print(f"{colorama.Fore.GREEN}Correctly matched URL: {i}\nWrited to file: {f.name}")
        print(headle_url)
        return render(request, "get/base.html", {})
    except Exception as e:
        print(f"{colorama.Fore.RED}Catched an error: {e}")
        raise