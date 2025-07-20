import requests
import functools
import colorama

ENCODING = "utf-8"
VERIFY = True
TIME_OUT = 10

colorama.init(autoreset=True)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def fix_input(func):
    @functools.wraps(func)
    def fixed(inputs):
        if not inputs.startswith("http"):
            inputs = "http://" + inputs
        if not inputs.endswith("/"):
            inputs = inputs + "/"
        print(f"{colorama.Fore.GREEN}Fixed input: {inputs}")
        return func(inputs)
    return fixed

@fix_input
def get(inputs):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    ,
        'Content-Type': 'application/json'
    }
    request = requests.get(inputs, headers=headers, verify=VERIFY, timeout=TIME_OUT)
    request.encoding = ENCODING  # Set the encoding to utf-8
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
    request.encoding = ENCODING  # Set the encoding to utf-8
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request

def put(inputs, data=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        ,
        'Content-Type': 'application/json'
    }

    request = requests.put(inputs, json=data, headers=headers, verify=VERIFY, timeout=TIME_OUT)
    request.encoding = ENCODING  # Set the encoding to utf-8
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request

@fix_input
def delete(inputs):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        ,
        'Content-Type': 'application/json'
    }

    request = requests.delete(inputs, headers=headers, verify=VERIFY, timeout=TIME_OUT)
    request.encoding = ENCODING  # Set the encoding to utf-8
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request

@fix_input
def patch(inputs, data=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        ,
        'Content-Type': 'application/json'
    }

    request = requests.patch(inputs, json=data, headers=headers, verify=VERIFY, timeout=TIME_OUT)
    request.encoding = ENCODING  # Set the encoding to utf-8
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request


@fix_input
def head(inputs):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    ,
        'Content-Type': 'application/json'
    }

    request = requests.head(inputs, headers=headers, verify=VERIFY, timeout=TIME_OUT)
    request.encoding = ENCODING  # Set the encoding to utf-8
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request

@fix_input
def options(inputs):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    ,
        'Content-Type': 'application/json'
    }

    request = requests.options(inputs, headers=headers, verify=VERIFY, timeout=TIME_OUT)
    request.encoding = ENCODING  # Set the encoding to utf-8
    print(f"{colorama.Fore.GREEN}Request status code: {request.status_code}")
    return request
