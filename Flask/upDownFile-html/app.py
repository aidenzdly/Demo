from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request,send_from_directory,url_for,send_file
import time
import os
import re
import base64
import json
from io import BytesIO
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule('/static/upload/<filename>','upload_img',build_only=True)
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 用于测试上传，稍后用到
@app.route('/test/upload')
def upload_test():
    return render_template('upload.html')


# 上传文件
@app.route('/api/upload', methods=['POST','GET'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files.getlist('myfile')  # 从表单的file字段获取文件，myfile为该表单的name值
    print(f)
    index = 0
    for a in f:
        if a and allowed_file(a.filename):  # 判断是否是允许上传的文件类型
            index += 1
            fname = secure_filename(a.filename)
            ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
            new_filename = str(index) + '.' + ext  # 修改了上传的文件名
            a.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        else:
            return jsonify({"error":"upload failed!"})
    return jsonify ({"errno": 0, "msg": "upload successfully!"})


# 打包下载目录全部文件
@app.route('/download',methods=['POST','GET'],strict_slashes=False) # False:url加不加斜杠都行
def download():
    filePath = 'static/upload'
    dirpath = os.path.join(app.root_path,filePath)
    # path = r'D:\Tensorflow_files\imgs'
    downloadPath = r'/imgs'
    completeDirs = [os.path.join(dirpath,i) for i in os.listdir(dirpath)]
    for perDir in completeDirs:
        imgNameList = re.findall(r'[^\\]+?\.jpg',perDir)
    if len(completeDirs) == 1:
        return send_from_directory(dirpath,imgNameList[0],as_attachment=True)
    else:
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, "a", zipfile.ZIP_DEFLATED) as zf:
            for _file in completeDirs:
                fnameList = re.findall(r'[^\\]+?\.jpg', _file)
                for fname in fnameList:
                    ffname = downloadPath +'/' + fname   # !!!!!
                    print("11111",ffname)
                    with open(os.path.join(dirpath, fname), 'rb') as fp:
                        # writestr支持将二进制数据直接写入到压缩文档
                        # ffname为图片保存在本地路径
                        zf.writestr(ffname, fp.read())
        memory_file.seek(0)
        return send_file(memory_file, attachment_filename='filename.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5050,debug=True)