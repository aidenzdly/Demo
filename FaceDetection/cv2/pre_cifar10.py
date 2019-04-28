import requests
import base64
import json
import cv2
import numpy as np
import time


# 列举最多分类个数
top = 5
# 预测具体类别,将其转化为array的多维数组格式
# pre_classes = np.array(["飞机","汽车","鸟","猫","鹿","狗","青蛙","马","船","卡车"])

def get_input_data(image_path):
    # 读取图片
    image_data = cv2.imread(image_path)
    # 转换为模型需要打图片大小
    image_data = cv2.resize(image_data, (32, 32))
    # bgr 转 rgb （opencv读取图片的默认像素排列是bgr，和多种软件不一致，转为rgb）
    image_data = image_data[:, :, ::-1]
    # 转换为模型需要的浮点类型
    image_data = image_data.astype(np.float32)
    # 此时的image_data 类型为numpy 是无法直接包装到json请求信息中的，需要转换为数组
    image_data = image_data.tolist()

    return image_data

#图片路径
image_paths = ['./mayun.jpg']
# image_paths = [str(input("请输入单张图片路径，并进行分类预测："))]
# data数据为json格式，数据内容格式为[{"a":b}]
instances = []
for i in image_paths:
    per_image_instance = {"input_image":get_input_data(i)}
    print(per_image_instance)
    instances.append(per_image_instance)

#restful url
# URL = "http://端口:地址/v1/models/test_model:predict"
URL = "http://192.168.4.140:8501/v1/models/facenet:predict"
#请求json头
headers = {"content-type": "application/json"}
#请求数据
body = {
    "signature_name": "serving_default",
    "instances": instances
    }
# dumps将python对象转为json对象，便于网络间传输
r = requests.post(URL, data=json.dumps(body), headers = headers,timeout = 30)

# start_time = time.time()
# loads将json对象转为python对象，后续对数据处理
result = json.loads(r.text)
# 字典key(predictions)对应的类别及概 率值，然后转为array格式的多维数组
scores = np.array(result["predictions"][0])
# end_time = time.time()
# np.argsort返回的是数组从小到大的索引值
scores_desc = np.argsort(scores)
print(scores_desc)
# [scores_desc][::-1]倒序排列,[:top]取前top个值
scores = scores[scores_desc][::-1][:top]
print(scores)
# 根据对应的下标索引，取出相对应的类别
# classes = pre_classes[scores_desc][::-1][:top]
# 通过zip函数，将对象中对应的元素 一一打包成元祖返回，取前5位小数
# meta = [(i,"%.5f" %j) for i,j in zip(classes,scores)]
# print(r.text)
# print("预测最有可能类别及概率(倒序)分别为: ------->",meta )