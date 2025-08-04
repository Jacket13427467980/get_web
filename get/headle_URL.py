import re

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

def headle_text(text: str, base_url: str):
    headle1 = headle(text,1)
    headle2 = [base_url + url for url in headle(text, 2)]
    headle3 = headle(text, 3)
    return list(set(headle1) | set(headle2) | set(headle3))
