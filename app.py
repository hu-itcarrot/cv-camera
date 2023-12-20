import numpy as np
from flask import request, render_template, url_for, redirect
from lib.core import YoLov5TRT
from configs import *
from lib.camera import *

basedir = os.path.abspath(os.path.dirname(__file__))

yolov5_wrapper = YoLov5TRT(engine_file_path)


@app.route('/detect', methods=['GET', 'POST'])
def detect_img():
    c_id = request.values.get("c_id")
    c_posi = request.values.get("c_posi")
    class_id = request.values.get("class_id")
    recive_url = request.values.get("recive_url")
    c_time = request.values.get("c_time")
    file = request.files['file']
    img = file.read()
    img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR) 
    label = yolov5_wrapper.infer(img, c_id, class_id, c_posi, recive_url, c_time)
    print(f'\n\n{c_id}-{label}\n\n')
    return label

@app.route('/save', methods=['GET', 'POST'])
def save():
    c_id = request.values.get("videoId")
    c_posi = request.values.get("diagPosition")
    class_id = request.values.get("faultLevel")
    diagTime = request.values.get("diagTime")
    file = request.files['file']
    img = file.read()
    img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR) 
    cv2.imwrite(f'./images/test/test-{c_id}.jpg', img)
    return 'Hello World!'




@app.route('/')
def index():
    items = Data.query.all()
    state = Data.query.filter_by(id=1).first().camera_url
    return render_template('index.html', items=items[1:], state=state)


@app.route('/del/<id>')
def del_data(id):
    d = Data.query.filter_by(id=int(id)).first()
    db.session.delete(d)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        c_id = int(request.form.get('c-id'))
        camera_url = request.form.get('c-ad')
        camera_posi = request.form.get('c-posi')
        recive_url = request.form.get('c-up')
        class_id = request.form.get('c-class')
        camera_time = request.form.get('c-time')
        print(recive_url)
        db.session.add(
            Data(c_id=c_id, camera_url=camera_url, camera_posi=camera_posi, class_id=class_id, recive_url=recive_url, camera_time=camera_time))
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/pause')
def pause():
    Data.query.filter_by(id=1).first().camera_url = 'False'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/start')
def start():
    Data.query.filter_by(id=1).first().camera_url = 'True'
    db.session.commit()
    threads = []
    data = Data.query.all()
    for i, e in enumerate(data[1:]):
        threads.append(inferThread(Camera(e.c_id, e.camera_posi, e.class_id, e.camera_time, e.camera_url, e.recive_url)))
    for e in threads:
        e.start() 
    return redirect(url_for('index'))





if __name__ == '__main__':
    if not os.path.exists('./data.sqlite'): 
        db.create_all()
        db.session.add(Data(c_id=-1, camera_url='True', camera_posi='True',  class_id='True', recive_url='True', camera_time=2))
        db.session.commit()
    app.run(host='0.0.0.0', port=5000)
