from urllib import request
from urllib.parse import urlencode

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
wd = {"wd": "中国"}
wd = urlencode(wd).encode(encoding='UTF8')
url = "http://www.baidu.com/s?"
req = request.Request(url, wd, headers=headers)
response = request.urlopen(req)
print(response)
res = response.read().decode()
print(res)