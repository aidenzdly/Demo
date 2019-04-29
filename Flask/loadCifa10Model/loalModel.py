from flask import request, Flask,send_from_directory,send_file,url_for
import os
from  io import BytesIO
import zipfile
from keras.models import load_model
import time
import keras
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np


app = Flask(__name__)
label = ['飞机', '汽车', '鸟', '猫', '鹿', '狗', '青蛙', '马', '船', '卡车']

@app.route('/loadmodel',methods=['POST'])
def loadmodel():
    # imgFiles = request.files['file']
    keras.backend.clear_session()
    model = load_model(r'h5Model/retrain_model.h5')
    # perImgPath = request.form['perImgPath']
    loadImgDir = 'static/upload1/'
    loadImgPath = [os.path.join(loadImgDir, i) for i in os.listdir(loadImgDir)]
    for perImgPath in loadImgPath:
        perImgName = perImgPath.split('/')[-1]
        if perImgPath == None:
            return '请输入正确的图片路径！'
        if not os.path.exists(perImgPath):
            return "filePath not exist!"
        imgRead = Image.open(perImgPath).resize((32,32),Image.BILINEAR)
        x = np.array(imgRead,dtype='float32')
        x = np.expand_dims(x,axis=0)
        results = model.predict(x)
        label_result = label[np.argmax(results)]
        print(f'预测最有可能的类别:{label_result},概率为{np.max(results)}',)

        imgRead = cv2.imread(perImgPath)
        fontPath = 'static/font/simsun.ttc'
        font = ImageFont.truetype(fontPath, 15)
        imgPil = Image.fromarray(imgRead)
        draw = ImageDraw.Draw(imgPil)
        # 回执文字信息
        draw.text((100, 50), '预测最有可能类别为：%s,概率为：%.2f%%' %
                            (label_result,np.max(results)*100),font=font,
                            fill=(0,0,0))
        imgRead = np.array(imgPil)
        cv2.imwrite(('static/imgwords/%s'%perImgName),imgRead)
    return '加载模型成功！'


if __name__ == "__main__":
    app.run(threaded=True)