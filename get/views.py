from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import colorama
from . import headle_URL
from . import get_requests
import json
import logging

logger = logging.getLogger(__name__)
RESPONSES = []


# Create your views here.
colorama.init(autoreset=True)

def index(request):
    return render(request, 'get/base.html', {})

def get(request, _website):
    import urllib.parse
    website = ""
    for i in _website:
        website += i
    decoded_website = urllib.parse.unquote(website)
    print(f"Original URL: {website}, Decoded URL: {decoded_website}")

    print(f"{colorama.Fore.GREEN}Fetching URL: {decoded_website}")
    try:
        print(f"{colorama.Fore.YELLOW}Starting to fetch {decoded_website}...")
        responses = headle_URL.multiple_requests([decoded_website], 
                                                 """json.loads(request.body.decode("utf-8"))"""
                                                )
        print(f"{colorama.Fore.GREEN}Fetched {len(responses)} responses.")
        RESPONSES.extend(responses)
        json.dumps(responses, indent=4)
        return render(request, "get/base.html", {"responses": RESPONSES})
    except Exception as e:
        print(f"{colorama.Fore.RED}Catched an error: {e}")
        raise
        return render(request, "get/base.html")


@require_http_methods(["GET"])
def get_response(request, url):
    import urllib.parse
    website = ""
    for i in url:
        website += i
    decoded_website = urllib.parse.unquote(website)
    print(f"Original URL: {website}, Decoded URL: {decoded_website}")
    try:
        json_data = json.loads(open("./get/templates/get/index.json", "r").read())
        headers = json_data.get("headers", {})
        response = get_requests.get(decoded_website, json_data, headers)
        return JsonResponse({"response": response})
    except Exception as e:
        logger.error(e)
        return JsonResponse({"response": str(e)}, status=400)