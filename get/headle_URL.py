"""Headle the URL and get the response"""

import re
from requests import Response
import colorama

try:
    from . import get_requests
except ImportError:
    import get_requests
colorama.init(autoreset=True)

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

def headle_text(response: Response) -> set:
    total_return = set()

    # 展平 findall 的结果，确保都是字符串
    def flatten_findall(findall_result):
        flat = []
        for item in findall_result:
            if isinstance(item, (list, tuple)):
                for subitem in item:
                    if isinstance(subitem, str) and subitem:
                        flat.append(subitem)
            elif isinstance(item, str) and item:
                flat.append(item)
        return flat

    headle1 = flatten_findall(headle(response.text, 1))
    headle2 = [f"{response.url if not response.url.endswith('/') else response.url[:-1]}{url}" for url in headle(response.text, 2) if isinstance(url, str)]
    headle3 = flatten_findall(headle(response.text, 3))
    total_return.update(set(headle1) | set(headle2) | set(headle3))

    return total_return
    
requested_urls = list()
requested_objects:list[Response] = list()
def multiple_requests(urls: list,
                      headers:any=None,
                      data:any=None,
                      verify:bool=get_requests.VERIFY,
                      requester: callable=get_requests.get,
                      headler: callable=headle_text):
    global requested_urls, requested_objects

    print(f"{colorama.Fore.LIGHTMAGENTA_EX}Is ready to fetch URLs: {urls}")
    responses: list[Response] = list()
    for url in urls:
        print(f"fetching {url}", end=" ")
        try:
            if url not in requested_urls:
                response: Response = requester(url)
        except Exception as e:
            print(f"{colorama.Fore.RED}Error fetching URL Error: {e}")
            # raise
        else:
            if response.status_code >= 200 and response.status_code < 300:
                requested_objects.append(response)
            print(f"{colorama.Fore.GREEN}Successfully fetched URL and got: {response.reason} with status code {response.status_code}")
        finally:
            requested_urls.append(url)

    urls = set()
    for response in responses:
        urls.update(set(headler(response)))
    
    urls = list(set(urls | {response.url for response in requested_objects} | set(urls)))

    if urls:
        multiple_requests(urls, headers, data, verify, requester, headler)
        
    print(f"{colorama.Fore.GREEN}Successfully fetched all URLs {requested_objects}")
    return requested_objects