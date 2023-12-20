from configs import db
  

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer)
    camera_url = db.Column(db.String(200))
    camera_posi = db.Column(db.String(200))
    recive_url = db.Column(db.String(200))
    class_id = db.Column(db.String(50))
    camera_time = db.Column(db.Integer)


    def __init__(self, c_id, camera_url, camera_posi, class_id, recive_url, camera_time):

        self.c_id = c_id
        self.camera_url = camera_url
        self.class_id = class_id
        self.recive_url = recive_url
        self.camera_posi = camera_posi
        self.camera_time = camera_time

    def __repr__(self):
        # return f'id:{id}, camera_url:{}'
        return '<User %r>' % self.camera_url
