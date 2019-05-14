import requests
import os
import cv2
import tensorflow as tf


# requests方法请求上传文件接口
url = "http://127.0.0.1:5000/frame"
imgsBaseDir = 'static/imgs/'
imgsList = [os.path.join(imgsBaseDir, i) for i in os.listdir(imgsBaseDir)]
for perImgPath in imgsList:
    # pathDict可不用
    pathDict = {'perImgPath':perImgPath}
    perImgName = perImgPath.split('/')[-1]
    imgFiles = {'file':(perImgName,open(perImgPath,'rb'),'image/jpg|png')}
    r = requests.post(url,files=imgFiles,data=pathDict)
    print(r.text)

########################################################

# # # 请求方法一：requests请求下载接口
# # import requests
# url = "http://127.0.0.1:5000/download"
# # 文件保存路径，可放在工程或本地
# saveImgsPath = 'test/downloadImgs.zip'
# with open(saveImgsPath,'wb') as fp:
#     fp.write(requests.get(url).content)


# #请求方法二：urllib请求下载接口
# import urllib.request
# # url = "http://192.168.4.140/download"
# url = "http://127.0.0.1:5000/download"
# saveImgsPath = 'test/downloadImgs.zip'
# urllib.request.urlretrieve(url,saveImgsPath)

################################################

# # 请求上传模型接口
# import requests
import json
url = "http://127.0.0.1:5000/predict"
r = requests.post(url)
# a = json.loads(r.content.decode('utf-8'))
print(r.text)

# url = "http://0.0.0.0:8080/predict"
# r = requests.post(url)
# print(r.text)


# # 请求方法一：requests请求下载接口
import requests
url = "http://127.0.0.1:5000/download"
# 文件保存路径，可放在工程或本地
saveImgsPath = 'test/downloadImgs.zip'
with open(saveImgsPath,'wb') as fp:
    fp.write(requests.get(url).content)


######################################

#上传模型
# import requests
# url = "http://127.0.0.1:5000/uploadModel"
# modelPath = 'h5Model/retrain_model.h5'
# modelName = modelPath.split('/')[-1]
# print(modelName)
# modelFiles = {'model':(modelName,open(modelPath,'rb'))}
# r = requests.post(url,files=modelFiles)
# k = r.text
# print(k)