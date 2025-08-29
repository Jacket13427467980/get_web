"""Headle the URL and get the response"""

import re
from requests import Response
import colorama
import sys

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
    sys.setrecursionlimit(10000)
    responses: list[Response] = list(responses)
    total_return = list()
    
    for response in responses:
        headle1 = headle(response.text,1)
        headle2 = [response.url + url for url in headle(response.text, 2)]
        headle3 = headle(response.text, 3)
        total_return.append(list(set(headle1) | set(headle2) | set(headle3)))

    return total_return
    

def multiple_requests(urls: list,
                      headers:any=None,
                      data:any=None,
                      verify:bool=get_requests.VERIFY,
                      requester: callable=get_requests.get,
                      headler: callable=headle_text):
    requested_objects:list[Response] = list()
    print(f"{colorama.Fore.LIGHTMAGENTA_EX}Is ready to fetch URLs: {urls}")
    
    responses: list[Response] = []
    for url in urls:
        print(f"fetching {url}", end=" ")
        try:
            response = requester(url)
        except Exception as e:
            print(f"{colorama.Fore.RED}Error fetching URL Error: {e}")
            # raise
        else:
            print(f"{colorama.Fore.GREEN}Successfully fetched URL{responses}")
            requested_objects.extend(response)
            urls = [request.url for request in responses if request.url not in [obj.url for obj in requested_objects]]

    multiple_requests(urls, headers, data, verify, requester, headler)
        
    print(f"{colorama.Fore.GREEN}Successfully fetched all URLs {requested_objects}")
    return requested_objects