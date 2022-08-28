from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CrossroadVO import CrossroadVO
from project.com.vo.CameraVO import CameraVO




class VideoVO(db.Model):
    __tablename__='videomaster'
    videoId=db.Column('videoId',db.Integer,primary_key=True,autoincrement=True)
    videoFileName=db.Column('videoFileName',db.String(100))
    videoFilePath=db.Column('videoFilePath',db.String(100))
    videoDate=db.Column('videoDate',db.DATE)
    videoTime=db.Column('videoTime',db.TIME)
    videoFrom_LoginId=db.Column('videoFrom_LoginId',db.ForeignKey(LoginVO.loginId))
    video_AreaId=db.Column('video_AreaId',db.Integer,db.ForeignKey(AreaVO.areaId))
    video_CrossroadId=db.Column('video_CrossroadId',db.Integer,db.ForeignKey(CrossroadVO.crossroadId))
    video_CameraId=db.Column('video_CameraId',db.Integer,db.ForeignKey(CameraVO.cameraId))
    detectionStatus = db.Column('detectionStatus', db.String(15))
    detectionFileName=db.Column('detectionFileName',db.String(100))
    detectionFilePath=db.Column('detectionFilePath',db.String(100))


    def as_dict(self):
        return {
            'videoId':self.videoId,
            'videoFileName':self.videoFileName,
            'videoFilePath':self.videoFilePath,
            'videoDate':self.videoDate,
            'videoTime':self.videoTime,
            'videoFrom_LoginId':self.videoFrom_LoginId,
            'video_AreaId':self.video_AreaId,
            'video_CrossroadId':self.video_CrossroadId,
            'video_CameraId':self.video_CameraId,
            'detectionStatus': self.detectionStatus,
            'detectionFileName':self.detectionFileName,
            'detectionFilePath':self.detectionFilePath

        }

db.create_all()
