# 请求上传模型接口
import requests
url = "http://127.0.0.1:5000/loadmodel"
r = requests.post(url)
print(r.text)