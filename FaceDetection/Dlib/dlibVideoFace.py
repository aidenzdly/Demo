import dlib
import cv2

# # detector表示获得脸部位置检测器，返回值为矩形
detector = dlib.get_frontal_face_detector()
# cv2加载上传视频文件：参数为0，打开笔记本内置摄像头
camera = cv2.VideoCapture(r'C:\Users\T470P\Desktop\video\mayun.mp4')
if not camera.isOpened():
    print("cannot open camear")
    exit(0)
    
# 改变图片的亮度与对比度
def relight(frame, light=1, bias=0):
    w = frame.shape[1]
    h = frame.shape[0]
    # image = []
    for i in range(0, w):
        for j in range(0, h):
            for c in range(3):
                tmp = int(frame[j, i, c] * light + bias)
                if tmp > 255:
                    tmp = 255
                elif tmp < 0:
                    tmp = 0
                frame[j, i, c] = tmp
    return frame

face_gap = 0
frame_index = 0
while True:
    frame_index += 1
    # ret返回值为True，frame返回值为图片数组
    ret, frame = camera.read()
    if not ret:
        break
    if face_gap == 0:
        # cv2.rectangle 会在传入图像上做绘图，必须再复制一个专门用于画图的图像，否则裁剪的人脸小图周围会有之前画的边框
        # 复制图像
        draw_frame = frame.copy()
        # cv2.cvtColor()进行色彩空间的转换，参数:1.原图 2.BGR和RGB的转化
        # dets 为object
        dets = detector(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1)
        print("Number of faces detected: {}".format(len(dets)))
        for i, face in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} ".format(
                i, face.left(), face.top(), face.right(), face.bottom()))
            # 参数：image，plt1，pt2，color
            cv2.rectangle(draw_frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 1)
            # frame图片数组，crop_image为检测识别到的人脸
            crop_image = frame[face.top():face.bottom(), face.left():face.right()]
            # print(crop_image)
            # 将检测到的人脸保存在相应的路径中
            # cv2.imwrite(r"D:\Pic\\" + str(frame_index) + "_" + str(i) + '.jpg', crop_image)
            cv2.imwrite(r"D:\Pic2\\" + str(frame_index) + "_" + str(i) + '.jpg', crop_image)
        if len(dets) > 0:
            # 检测到了有人脸，则跳过5帧再检测人脸，减少重复
            face_gap = face_gap + 10
        # 展示视频，为每一帧的图片
        cv2.imshow("Camera", draw_frame)
        # 给定1ms等待用户按键触发
        key = cv2.waitKey(1)
        # 等待时间1ms,如果在这个时间段内,按下ESC(Ascii码为27),则跳出循环
        if key == 27:
            break
    else:
        face_gap -= 1

cv2.destroyAllWindows()
