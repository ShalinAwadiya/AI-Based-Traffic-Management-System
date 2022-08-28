from project import db
from project.com.vo.CrossroadVO import CrossroadVO
from project.com.vo.AreaVO import AreaVO


class CameraVO(db.Model):
    __tablename__ = 'cameramaster'
    cameraId = db.Column('cameraId', db.Integer, primary_key=True, autoincrement=True)
    cameraCode = db.Column('cameraCode', db.String(100))
    camera_CrossroadId = db.Column('camera_CrossroadId', db.ForeignKey(CrossroadVO.crossroadId))
    camera_AreaId = db.Column('camera_AreaId', db.ForeignKey(AreaVO.areaId))

    def as_dict(self):
        return {
            'cameraId': self.cameraId,
            'cameraCode': self.cameraCode,
            'camera_CrossroadId': self.camera_CrossroadId,
            'camera_AreaId': self.camera_AreaId
        }


db.create_all()
