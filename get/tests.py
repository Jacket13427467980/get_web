from django.test import TestCase

# Create your tests here.

import headle_URL
print(headle_URL.WORD1.findall("http://github.com git.git?name=git#web"))
print(headle_URL.WORD2.findall("/git/git.git?w=w#web"))
print(headle_URL.WORD3.findall("127.0.0.1:8000"))
