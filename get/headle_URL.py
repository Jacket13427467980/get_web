"""Headle the URL and get the response"""

import re
import shutil
from requests import Response
import colorama
from pathlib import Path
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

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
    
WEB_TEMPLATES_DIR = Path("web_templates")
WEB_TEMPLATES_DIR.mkdir(exist_ok=True)

def url_to_filename(url: str) -> str:
    """将URL安全地转换为文件名（使用md5哈希）"""
    h = hashlib.md5(url.encode('utf-8')).hexdigest()
    return h

def multiple_requests(urls: list,
                      headers:any=None,
                      data:any=None,
                      verify:bool=get_requests.VERIFY,
                      requester: callable=get_requests.get,
                      headler: callable=headle_text):
    requested_urls = list()
    requested_objects:list[Response] = list()
    shutil.rmtree(WEB_TEMPLATES_DIR, ignore_errors=True)
    WEB_TEMPLATES_DIR.mkdir(exist_ok=True)


    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_url = {executor.submit(requester, url, headers=headers, data=data, verify=verify): url for url in urls if url not in requested_urls}
        while future_to_url:
            for future in as_completed(future_to_url):
                url = future_to_url.pop(future)
                try:
                    response: Response = future.result()
                except Exception as e:
                    print(f"{colorama.Fore.RED}Error fetching URL {url}: {e}")
                else:
                    requested_objects.append(response)
                    print(f"{colorama.Fore.GREEN}Successfully fetched URL {url} and got: {response.reason} with status code {response.status_code}")
                    new_urls = list(set(headler(response)))
                    if new_urls:
                        print(f"{colorama.Fore.CYAN}Discovered new URLs from {url}: {len(new_urls)}")
                        urls.extend(new_urls)
                        urls = list(set(urls))
                    # Ensure directory exists
                    safe_filename = url_to_filename(response.url)
                    file_path = WEB_TEMPLATES_DIR / safe_filename
                    file_path.touch()
                    file_path.write_text(response.text, encoding=response.encoding if response.encoding else "utf-8")
                finally:
                    requested_urls.append(url)
                    print(f"{colorama.Fore.YELLOW}Remaining URLs to fetch: {len(requested_urls)}")
            future_to_url = {executor.submit(requester, url, headers=headers, data=data, verify=verify): url for url in urls if url not in requested_urls}

    print(f"{colorama.Fore.GREEN}Successfully fetched all URLs {requested_objects}")
    return requested_objects