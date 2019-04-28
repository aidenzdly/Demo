import dlib         # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import cv2          # 图像处理的库OpenCv

# Dlib 预测器
# 加载Landmark人脸68个关键点的dat模型库
# detector表示获得脸部位置检测器，返回值为矩形
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/dlib/shape_predictor_68_face_landmarks.dat')

# 读取图像
path = "data/images/faces_for_test/"
# cv2和Image打开读取图片的方式有区别
img = cv2.imread(path+"test_faces_1.jpg")

# Dlib 检测
faces = detector(img, 1)
print("人脸数：", len(faces), "\n")


# 记录人脸矩阵大小
height_max = 0
width_sum = 0

# 计算要生成的图像 img_blank 大小
for k, d in enumerate(faces):

    # 计算矩形大小
    # (x,y), (宽度width, 高度height)
    pos_start = tuple([d.left(), d.top()])
    pos_end = tuple([d.right(), d.bottom()])

    # 计算矩形框大小
    height = d.bottom()-d.top()
    width = d.right()-d.left()

    # 处理宽度
    width_sum += width

    # 处理高度
    if height > height_max:
        height_max = height
    else:
        height_max = height_max

# 绘制用来显示人脸的图像的大小
print("窗口大小："
      , '\n', "高度 / height:", height_max
      , '\n', "宽度 / width: ", width_sum)

# 生成用来显示的图像
img_blank = np.zeros((height_max, width_sum, 3), np.uint8)

# 记录每次开始写入人脸像素的宽度位置
blank_start = 0

# 将人脸填充到img_blank
for k, d in enumerate(faces):

    height = d.bottom()-d.top()
    width = d.right()-d.left()
    # 填充
    for i in range(height):
        for j in range(width):
            img_blank[i][blank_start+j] = img[d.top()+i][d.left()+j]
    # 调整图像:blank_start:窗口宽度；height:窗口高度
    blank_start += width
    # print(blank_start)

# cv2.nameWindow("窗口标题",默认参数)，创建窗口以供显示图像
cv2.namedWindow("img_faces")#, 2)
# 显示图像
cv2.imshow("img_faces", img_blank)
# waitKey(0)表示按任意键继续；waitKey()函数的功能是不断刷新图像
cv2.waitKey(0)