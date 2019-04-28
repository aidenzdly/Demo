import dlib  # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import cv2  # 图像处理的库OpenCv
import os  # 文件操作模块
from PIL import Image  # 图像处理的基本模块
from tqdm import tqdm  # tqdm:python的终端进度条工具

# 读取图像的路径
# path_read = r"data/images/faces_for_test/test_faces_1.jpg"
# img = cv2.imread(path_read+"timg.jpg")

# 用来存储生成的单张人脸的路径
path_save = r"C:/Users/T470P/Desktop/test//"
# 读取代开图片
L_path = r"C:\Users\T470P\Desktop\timg.jpg"
L_image = Image.open(L_path)
# 将图片转为RGB模式(否则报错)
out = L_image.convert("RGB")
# 将图片格式转为数组类型传入(否则报错)
img = np.array(out)
print(img)


# Delete old images
# 清除生成图片文件夹内的文件
def clear_images():
    imgs = os.listdir(path_save)
    for img in imgs:
        os.remove(path_save + img)
    print("clean finish", '\n')


clear_images()

# root_path='data'
# examples = ['data/images/faces_for_test/test_faces_1.jpg','data/images/faces_for_test/test_faces_2.jpg']
# for item in examples:
#     L_image = Image.open(item)
#     out = L_image.convert("RGB")
#     img = np.array(out)


# Dlib 预测器
# 加载Landmark人脸68个关键点的dat模型库
# detector表示获得脸部位置检测器，返回值为矩形
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/dlib/shape_predictor_68_face_landmarks.dat')

# Dlib 检测人脸
faces = detector(img, 1)
print("人脸数：", len(faces), '\n')
# 用enumerate将数组组合为一个索引序列，同时列出数据下标和数据
for k, d in enumerate(faces):
    # 计算矩形大小
    # (x,y), (宽度width, 高度height)
    # pos_start:矩形左上角; pos_end:矩形右下角
    pos_start = tuple([d.left(), d.top()])
    pos_end = tuple([d.right(), d.bottom()])

    # 计算矩形框大小
    height = d.bottom() - d.top()
    width = d.right() - d.left()
    print(height)
    print(width)

    # 根据人脸大小生成空的图像
    # 在skimage中，一张图片就是一个简单的numpy数组，一张图片的像素范围是[0,255]，默认是uint8
    # np.zeros:生成一个3维全零数组，相当于生成空的图像
    img_blank = np.zeros((height, width, 3), np.uint8)

    for i in range(height):
        for j in range(width):
            # 将识别的人脸以数组的格式保存
            img_blank[i][j] = img[d.top() + i][d.left() + j]

    # cv2.imshow("face_"+str(k+1), img_blank)

    # 存在本地
    print("Save to:", path_save + "img_face_" + str(k + 1) + ".jpg")
    cv2.imwrite(path_save + "img_face_" + str(k + 1) + ".jpg", img_blank)
