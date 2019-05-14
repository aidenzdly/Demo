from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, send_from_directory, send_file
import time
import os
import base64
import json
import re
from io import BytesIO
import zipfile
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras import backend as K
import tensorflow as tf
import requests
import json
from pypinyin import lazy_pinyin

# 文件上传
app = Flask(__name__)
label = ['飞机', '汽车', '鸟', '猫', '鹿', '狗', '青蛙', '马', '船', '卡车']


# uwsgi不支持先加载模型，在进行预测
# 我们需要重新定义我们的度量函数，
# 从而在加载模型时使用它
#def auc(y_true, y_pred):
    #auc = tf.metrics.auc(y_true, y_pred)[1]
    #K.get_session().run(tf.local_variables_initializer())
    #return auc

# 加载模型，传入自定义度量函数
# 保证tf模型和flask处于同一个线程中

#global graph
#graph = tf.get_default_graph()
#model = load_model(r"h5Model/retrain_model.h5", custom_objects={'auc': auc})
## 先用模型预测一遍，不会报core：3错误
#graph = tf.get_default_graph()
#model = load_model(r"h5Model/retrain_model.h5")
#a = model.predict((np.random.random((1,32,32,3))*255).astype(np.int8))
#label = label[np.argmax(a)]


def get_input_data(image_path):
    # 读取图片(含中文)
    cv_img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
    # image_data = cv2.imread(image_path)  # 英文
    # 转换为模型需要打图片大小
    image_data = cv2.resize(cv_img, (32, 32))
    # bgr 转 rgb （opencv读取图片的默认像素排列是bgr，和多种软件不一致，转为rgb）
    image_data = cv2.cvtColor(image_data,cv2.COLOR_RGBA2BGR)
    # 转换为模型需要的浮点类型
    image_data = image_data.astype(np.float32)
    # 此时的image_data 类型为numpy 是无法直接包装到json请求信息中的，需要转换为数组
    image_data = image_data.tolist()
    return image_data


def sort_pinyin(hanzi_list):
    '''
    按汉字首字母拼音排序
    '''
    hanzi_list_pinyin=[]
    hanzi_list_pinyin_alias_dict={}
    for single_str in hanzi_list:
        py_r = lazy_pinyin(single_str)
        single_str_py=''
        for py_list in py_r:
            single_str_py=single_str_py+py_list
        hanzi_list_pinyin.append(single_str_py)
        hanzi_list_pinyin_alias_dict[single_str_py]=single_str
    hanzi_list_pinyin.sort()
    sorted_hanzi_list=[]
    for single_str_py in hanzi_list_pinyin:
        sorted_hanzi_list.append(hanzi_list_pinyin_alias_dict[single_str_py])
    return sorted_hanzi_list


def correct_path(dir):
    '''
    顺序排列目录
    '''
    # loadImgPath = [os.path.join(dir, i) for i in os.listdir(dir)]
    namesImg = os.listdir(dir)
    characterListPath = list(filter(lambda elm: re.search(r'^[\u4e00-\u9fa5]', elm), namesImg))
    numberListPath = list(filter(lambda elm: re.search(r'^[0-9]', elm), namesImg))
    engPath = set(namesImg) - set(characterListPath) - set(numberListPath)
    engPath = sorted(list(engPath))
    characterListPath = sort_pinyin(characterListPath)
    numberListPath = sorted(numberListPath)
    correctPath = numberListPath + engPath + characterListPath
    correctPath = [os.path.join(dir, i) for i in correctPath]
    return correctPath



@app.route("/frame", methods=['POST'])
def get_frame():
    s1 = time.time()
    upload_file = request.files['file']
    fileName = upload_file.filename
    filePath = os.path.join('static/upload1/' + fileName)
    if upload_file:
        upload_file.save(filePath)
        e1 = time.time()
        print("上传图片时间：",(e1-s1))
        print('图片上传路径成功！')
        return 'upload images successfully!'
    else:
        return 'upload failed!'


# 打包下载目录全部文件
@app.route('/download', strict_slashes=False)  # False:url加不加斜杠都行
def download():
    filePath = 'static/imgwords/'
    dirpath = os.path.join(app.root_path, filePath)
    # path = r'D:\Tensorflow_files\imgs'
    downloadPath = r'/imgs'
    completeDirs = [os.path.join(dirpath, i) for i in os.listdir(dirpath)]
    for perDir in completeDirs:
        imgName = perDir.split('/')[-1]
    if len(completeDirs) == 1:
        return send_from_directory(dirpath, imgName, as_attachment=True)
    else:
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, "a", zipfile.ZIP_DEFLATED) as zf:
            for _file in completeDirs:
                fname = _file.split('/')[-1]
                ffname = downloadPath + '/' + fname
                with open(os.path.join(dirpath, fname), 'rb') as fp:
                    # writestr支持将二进制数据直接写入到压缩文档
                    # ffname为图片保存在本地路径
                    zf.writestr(ffname, fp.read())
        memory_file.seek(0)
        return send_file(memory_file, attachment_filename='filename.zip', as_attachment=True)

@app.route('/predict',methods=['POST'])
def predict():
    # keras.backend.clear_session()
    try:
        loadImgDir = './static/upload1/'
        correctPath = correct_path(loadImgDir)
        instances = []
        for perImgPath in correctPath:
            perImgName = perImgPath.split('/')[-1]
            del instances[:]
            per_image_instance = {"input_image": get_input_data(perImgPath)}
            instances.append(per_image_instance)
        # print(instances)
            url = "http://192.168.4.140:8501/v1/models/cifar10:predict"
            headers = {"content-type": "application/json"}
            body = {
                "signature_name": "serving_default",
                "instances": instances
            }
            r = requests.post(url, data=json.dumps(body), headers=headers, timeout=30)
            result = json.loads(r.text)
            scores = np.array(result["predictions"][0])
            label_result = label[np.argmax(scores)]
            print(f'预测最有可能的类别:{label_result},概率为{np.max(scores)}', )

            cv_img = cv2.imdecode(np.fromfile(perImgPath, dtype=np.uint8), -1)
            # imgRead = cv2.imread(perImgPath)   # cv2不能直接读中文，需要编码
            text = '预测最有可能的类别:：%s,概率为：%.2f%%' %(label_result, np.max(scores) * 100)
            text_origin = (100, 50)
            colors = (0,0,0)
            # cv2只能写入英文，中文乱码
            # imgRead = cv2.putText(cv_img, text, text_origin, cv2.FONT_HERSHEY_SIMPLEX, text_scale, colors, 1)
            fontPath = 'static/font/simsun.ttc'
            font = ImageFont.truetype(fontPath, 15)
            imgPil = Image.fromarray(cv_img)
            draw = ImageDraw.Draw(imgPil)
            # 回执文字信息
            draw.text(text_origin,text , font=font,fill=colors)
            imgRead = np.array(imgPil)
            # 针对中文转义
            cv2.imencode('.jpg', imgRead)[1].tofile('static/imgwords/%s' % perImgName)
            # cv2.imwrite(('static/imgwords/%s' % perImgName), imgRead) # 英文
        return "Predict Successfully!！"
    except Exception as e:
        return "请输入正确的图片路径!"


if __name__ == "__main__":
    app.run(threaded=True)
