from project import db
from project.com.vo.VideoVO import VideoVO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CrossroadVO import CrossroadVO
from project.com.vo.CameraVO import CameraVO
from project.com.vo.LoginVO import LoginVO


class VideoDAO:
    def insertVideo(self, videoVO):
        db.session.add(videoVO)
        db.session.commit()

    def userViewVideo(self,videoVO):
        videoList = db.session.query(VideoVO, CameraVO, CrossroadVO, AreaVO, LoginVO).join(CameraVO,VideoVO.video_CameraId == CameraVO.cameraId).join(CrossroadVO, VideoVO.video_CrossroadId == CrossroadVO.crossroadId).join(AreaVO,VideoVO.video_AreaId == AreaVO.areaId).join(LoginVO, VideoVO.videoFrom_LoginId == LoginVO.loginId).filter_by(loginId=videoVO.videoId).all()

        return videoList
    def adminViewVideo(self):
        videoList = db.session.query(VideoVO, CameraVO, CrossroadVO, AreaVO, LoginVO).join(CameraVO,VideoVO.video_CameraId == CameraVO.cameraId).join(CrossroadVO, VideoVO.video_CrossroadId == CrossroadVO.crossroadId).join(AreaVO,VideoVO.video_AreaId == AreaVO.areaId).join(LoginVO, VideoVO.videoFrom_LoginId == LoginVO.loginId).all()

        return videoList

    def deleteVideo(self, videoVO):
        videoList = VideoVO.query.get(videoVO.videoId)
        db.session.delete(videoList)
        db.session.commit()

        return videoList

    def editVideo(self, videoVO):
        videoList = VideoVO.query.filter_by(videoId=videoVO.videoId).all()

        return videoList

    def updateVideo(self, videoVO):
        db.session.merge(videoVO)
        db.session.commit()
