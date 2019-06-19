#coding: utf-8
from flask import *
import json
import time
import os
from werkzeug.utils import secure_filename
from lib import mnist_softmax, mnist_softmax_train, mnist_deep_train, mnist_deep
from cassandra.cluster import Cluster


app = Flask(__name__)

app.config['SECRET_KEY'] = 'MNIST_WEB'
# front end ui

global session

@app.route('/', methods=['GET'])
def index_page():
    return render_template("index.html")

@app.route('/api/softmax', methods=['POST'])
def softmax_api():
    global session
    if request.method == 'POST':
        BASE_DIR = os.path.dirname(__file__)
        #获取前端传输的文件(对象)
        f = request.files.get('image')
        # secure_filename：检测中文是否合法
        filename = f.filename
        # 验证文件格式（简单设定几个格式）
        types = ['jpg','png','gif']
        if filename.split('.')[-1] in types:
            # 保存图片
            relapath = 'static/upload/predict_{0}'.format(str(int(time.time())) + "." + filename.split('.')[-1])
            filepath = os.path.join(BASE_DIR, relapath)
            f.save(filepath)
            # 返回给前端结果
            result = int(mnist_softmax.run_predict(filepath))
            s = session
            s.execute("INSERT INTO mnistHistory (device, url, result, createtime) VALUES (1, %s, %s, %s)", [relapath, result, int(time.time())])
            return json.dumps({
                'code':200,
                'predict_result' : result,
                'file_path' : relapath
            })
        else:
            return json.dumps({'error':'文件格式不合法','code':400})

@app.route('/api/deep', methods=['POST'])
def deep_api():
    global session
    if request.method == 'POST':
        BASE_DIR = os.path.dirname(__file__)
        #获取前端传输的文件(对象)
        f = request.files.get('image')
        # secure_filename：检测中文是否合法
        filename = f.filename
        # 验证文件格式（简单设定几个格式）
        types = ['jpg','png','gif']
        if filename.split('.')[-1] in types:
            # 保存图片
            relapath = 'static/upload/predict_{0}'.format(str(int(time.time())) + "." + filename.split('.')[-1])
            filepath = os.path.join(BASE_DIR, relapath)
            f.save(filepath)
            # 返回给前端结果
            result = int(mnist_deep.run_predict(filepath))
            s = session
            s.execute("INSERT INTO mnistHistory (device, url, result, createtime) VALUES (1, %s, %s, %s)", [relapath, result, int(time.time())])
            return json.dumps({
                'code':200,
                'predict_result' : result,
                'file_path' : relapath
            })
        else:
            return json.dumps({'error':'文件格式不合法','code':400})

@app.route('/api/getHistory', methods=['GET'])
def get_history_api():
    global session
    rows = session.execute("select * from mnistHistory WHERE device = 1 ORDER BY createtime DESC LIMIT 10")
    result = []
    for row in rows:
        print(row)
        timeArray = time.localtime(int(row[1]))
        result.append({
            "url" : row[3],
            "result" : row[2],
            "createtime" : time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        })
    return jsonify({
        "code": 200,
        "data": result
    })

if __name__ == '__main__':
    global session
    if "CASSANDRA_HOST" in os.environ:
        print("[*] Creating Cassandra Session...")
        cluster = Cluster([os.environ['CASSANDRA_HOST']])
        session = cluster.connect()
    else:
        print("please set env CASSANDRA_HOST when launching docker.")
        print("    e.g. -e CASSANDRA_HOST=127.0.0.1:9160")
        exit(0)
    try:
        keyspacename = "mnist_web"
        session.execute("create keyspace %s with replication = {'class': 'SimpleStrategy', 'replication_factor': 1};" % keyspacename)
    except:
        pass
    # use keyspace; create a sample table
    session.set_keyspace(keyspacename)

    s = session
    try:
        s.execute("CREATE TABLE mnistHistory (device int, url text, result int, createtime int, PRIMARY KEY(device, createtime))")
    except:
        pass
    print("[*] Launching web server...")
    app.run(debug=True, host="0.0.0.0", port=80, threaded=True)
