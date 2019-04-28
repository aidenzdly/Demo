#coding:utf-8
from flask import request, Flask
import json
import numpy as np
import time
import cv2

# app = Flask(__name__)
#
# @app.route("/frame", methods=['POST','GET'])
# def get_frame():
#     start_time = time.time()
#     res = json.loads(request.data)
#     frame = eval(res["image"].decode("base64"))   # dtype为int32
#     frame = np.array(frame, dtype=np.uint8)
#     print("frame....",frame)
#     cv2.imwrite('/static/upload1',frame)
#     duration = time.time() - start_time
#     print('duration:[%.0fms]' % (duration*1000))
#     return '0000'
#
# if __name__ == "__main__":
#     app.run('0.0.0.0',port=5000)  #端口为8081



# @app.route('/frame',methods=['POST','GET'])
# def get_frame():
#     res = request.json
#     frame = eval(res['image'].decode('base64'))
#     frame = np.array(frame,dtype=np.uint8)
#     cv2.imshow('frame',frame)
#     cv2.waitkey(0)
#
# if __name__ == "__main__":
#     app.run('0.0.0.0',port=8081)



###############################################成功
from flask import request, Flask,send_from_directory,send_file
import os
from  io import BytesIO
import zipfile


app = Flask(__name__)

# 上传文件
@app.route("/frame", methods=['POST'])
def get_frame():
    upload_file = request.files['file']
    fileName = upload_file.filename
    # file_path = os.path.join('/home/images/'+ old_file_name)
    filePath = os.path.join('static/upload1/'+ fileName)
    if upload_file:
        upload_file.save(filePath)
        return 'upload images successfully!'
    else:
        return 'upload failed!'


# 打包下载文件
@app.route('/download',strict_slashes=False)
def download():
    filePath = 'static/upload1'
    dirpath = os.path.join(app.root_path,filePath)
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
                    zf.writestr(ffname, fp.read())
        memory_file.seek(0)
        return send_file(memory_file, attachment_filename='filename.zip', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True,threaded=True)