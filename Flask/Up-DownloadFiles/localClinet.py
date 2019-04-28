import requests
import os

# requests方法请求上传文件接口
url = "http://127.0.0.1:5000/frame"
imgsBaseDir = 'static/upload/'
imgsList = [os.path.join(imgsBaseDir, i) for i in os.listdir(imgsBaseDir)]
for perImgPath in imgsList:
    perImgName = perImgPath.split('/')[-1]
    imgFiles = {'file':(perImgName,open(perImgPath,'rb'),'image/jpg')}
    r = requests.post(url,files=imgFiles)
    print(r.text)

########################################################

# # 请求方法一：requests请求下载接口
# import requests
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