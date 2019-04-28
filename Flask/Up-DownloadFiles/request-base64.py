# 利用opencv发送接收图片--耗费时间
# ????
#coding:utf-8
import cv2
import json
import requests
import base64

img = cv2.imread("static/upload/mayun.jpg")
res = {
    "image": str(img.tolist()).encode('base64')
    }      # img是ndarray，无法直接用base64编码，否则会报错

_ = requests.post("http://0.0.0.0:5000/frame", data=json.dumps(res))
print("sss",_)