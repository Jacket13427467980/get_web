import re
from requests import Response
import colorama

from . import get_requests

WORD1 = re.compile(r"(?:([a-z]+:)?\/\/)?(?:[\w\d-]+\.)+[\w-]+(?::\d+)?(?:(?:\/[\w.-]*)+)?(?:\?[^#\s]*)?(?:#[^\s]*)?\/?")
WORD2 = re.compile(r"(?:\/(?!\.)(?!.*\/\.\.\/)[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*)+(?:\?[\w\-%.]+=[\w\-%.]*(?:&[\w\-%.]+=[\w\-%.]*)*)?(?:#[\w\-%.]+)?\/?")
WORD3 = re.compile(r"(?:[a-z]+:\/\/)?(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?::(6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0))?(?:(?:\/[\w.-]*)+)?(?:\?[^#\s]*)?(?:#[^\s]*)?\/?")

def headle(text: str, mode=1):
    if mode == 1:
        return WORD1.findall(text)
    elif mode == 2:
        return WORD2.findall(text)
    elif mode == 3:
        return WORD3.findall(text)

def headle_text(responses: Response|list[Response]):
    responses: list[Response] = list(responses)
    total_return = list()
    
    for response in responses:
        headle1 = headle(response.text,1)
        headle2 = [response.url + url for url in headle(response.text, 2)]
        headle3 = headle(response.text, 3)
        total_return.append(list(set(headle1) | set(headle2) | set(headle3)))

    return total_return
    

def multiple_requests(urls: str|list, requester: callable=get_requests.get, headler: callable=headle_text) -> list[Response]:
    urls = list(urls)
    requested_objects:list[Response] = list()

    try:
        requests = [requester(url) for url in urls if requester(url) not in requested_objects]
    except Exception as e:
        print(f"{colorama.Fore.RED}Error fetching URL Error: {e}")
        # raise
    else:
        print(f"{colorama.Fore.GREEN}Successfully fetched URL")
        requested_objects.extend(requests)
        urls = [request.url for request in requests if request.url not in [obj.url for obj in requested_objects]]

        multiple_requests(urls, requester, headler)
        
    return requested_objects