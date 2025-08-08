"""http requests module with fixed input handling and colorized output."""
from typing import Iterable
import requests
import functools
import colorama
from headle_URL import headle_text
from requests import Response

ENCODING = "utf-8"
VERIFY = True
TIME_OUT = 10
headers = {"sec-ch-ua": '''"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"''',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}


colorama.init(autoreset=True)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def fix_input(func):
    @functools.wraps(func)
    def fixed(inputs, data=None):
        if not inputs.startswith("http"):
            inputs = "http://" + inputs
        if not inputs.endswith("/"):
            inputs = inputs + "/"
        print(f"{colorama.Fore.GREEN}Fixed input: {inputs}")
        return func(inputs, data=data)
    return fixed

@fix_input
def get(inputs, data=None):
    request = requests.get(inputs, headers=headers, data=data, verify=VERIFY, timeout=TIME_OUT)
    # request.encoding = ENCODING  # Set the encoding to utf-8
    request.encoding = request.apparent_encoding 
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request

@fix_input
def post(inputs, data=None):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        ,
        'Content-Type': 'application/json'
    }

    request = requests.post(inputs, json=data, headers=headers, verify=VERIFY, timeout=TIME_OUT)
    # request.encoding = ENCODING  # Set the encoding to utf-8
    request.encoding = request.apparent_encoding
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request

def put(inputs, data=None):


    request = requests.put(inputs, json=data, headers=headers, verify=VERIFY, timeout=TIME_OUT)
    # request.encoding = ENCODING  # Set the encoding to utf-8
    request.encoding = request.apparent_encoding
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request

@fix_input
def delete(inputs, data=None):

    request = requests.delete(inputs, headers=headers, data=data, verify=VERIFY, timeout=TIME_OUT)
    # request.encoding = ENCODING  # Set the encoding to utf-8
    request.encoding = request.apparent_encoding
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request

@fix_input
def patch(inputs, data=None):

    request = requests.patch(inputs, json=data, data=data, headers=headers, verify=VERIFY, timeout=TIME_OUT)
    # request.encoding = ENCODING  # Set the encoding to utf-8
    request.encoding = request.apparent_encoding
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request


@fix_input
def head(inputs, data=None):

    request = requests.head(inputs, headers=headers, data=data, verify=VERIFY, timeout=TIME_OUT)
    # request.encoding = ENCODING  # Set the encoding to utf-8
    request.encoding = request.apparent_encoding
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request

@fix_input
def options(inputs, data=None):

    request = requests.options(inputs, headers=headers, data=data, verify=VERIFY, timeout=TIME_OUT)
    # request.encoding = ENCODING  # Set the encoding to utf-8
    request.encoding = request.apparent_encoding
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request

def multiple_requests(funt: callable , urls: str|list) -> Iterable[str, Response]:
    urls = list(urls)

    for url in urls:
        try:
            request: Response = funt(url)
        except Exception as e:
            print(f"{colorama.Fore.RED}Error fetching URL: {url} Error: {e}")
            continue
        else:
            yield (request.url, request)
            print(f"{colorama.Fore.GREEN}Successfully fetched URL: {url}")
            multiple_requests(funt, headle_text(request.text, url))
    