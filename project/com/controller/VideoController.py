from project import app
from flask import render_template, request, redirect, url_for, session
from project.com.vo.VideoVO import VideoVO
from project.com.dao.VideoDAO import VideoDAO
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.CrossroadDAO import CrossroadDAO
from project.com.dao.CameraDAO import CameraDAO
from project.com.controller.LoginController import adminLoginSession
from werkzeug.utils import secure_filename
import datetime
import os
from project.com.vo.LoginVO import LoginVO
from project.com.dao.LoginDAO import LoginDAO


@app.route('/user/loadVideo')
def userLoadVideo():
    try:
        if adminLoginSession() == 'user':
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            crossroadDAO = CrossroadDAO()
            crossroadVOList = crossroadDAO.viewCrossroad()

            cameraDAO = CameraDAO()
            cameraVOList = cameraDAO.viewCamera()

            return render_template('user/addVideo.html', areaVOList=areaVOList, crossroadVOList=crossroadVOList,
                                   cameraVOList=cameraVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/insertVideo', methods=['POST'])
def userInsertVideo():
    try:
        if adminLoginSession() == 'user':
            video_AreaId = request.form['video_AreaId']
            video_CrossroadId = request.form['video_CrossroadId']
            video_CameraId = request.form['video_CameraId']

            UPLOAD_FOLDER = 'project/static/adminResources/videos/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']
            videoFileName = secure_filename(file.filename)
            videoFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(videoFilePath, videoFileName))

            videoVO = VideoVO()
            videoDAO = VideoDAO()

            videoVO.videoFileName = videoFileName
            videoVO.videoFilePath = videoFilePath.replace('project', '..')
            videoVO.videoDate = datetime.datetime.now().date()
            videoVO.videoTime = datetime.datetime.now().time()
            videoVO.videoFrom_LoginId = session['session_loginId']
            videoVO.video_AreaId = video_AreaId
            videoVO.video_CrossroadId = video_CrossroadId
            videoVO.video_CameraId = video_CameraId
            videoVO.detectionStatus='Detect'

            videoDAO.insertVideo(videoVO)

            return redirect(url_for('userViewVideo'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/viewVideo')
def userViewVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO=VideoVO()
            videoDAO = VideoDAO()

            videoVO.videoId=session['session_loginId']
            videoVOList = videoDAO.userViewVideo(videoVO)

            return render_template('user/viewVideo.html', videoVOList=videoVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewVideo')
def adminViewVideo():
    try:
        if adminLoginSession() == 'admin':
            videoDAO = VideoDAO()
            videoVOList = videoDAO.adminViewVideo()
            return render_template('admin/viewVideo.html', videoVOList=videoVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/deleteVideo')
def userDeleteVideo():
    try:
        if adminLoginSession() == 'user':
            videoId = request.args.get('videoId')

            videoVO = VideoVO()
            videoDAO = VideoDAO()

            videoVO.videoId = videoId
            videoVOList = videoDAO.deleteVideo(videoVO)

            videoFilePath = videoVOList.videoFilePath.replace('..', 'project')
            videoFile = videoFilePath + videoVOList.videoFileName
            os.remove(videoFile)

            if videoVOList.detectionStatus=='Detected':
                detectionFilePath=videoVOList.detectionFilePath.replace('..','project')
                detectionFile=detectionFilePath + videoVOList.detectionFileName
                os.remove(detectionFile)

            return redirect(url_for('userViewVideo'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)



#Detection
@app.route('/user/detectVideo',methods=['GET'])
def adminDetectVideo():
    try:
        if adminLoginSession() == 'user':

            videoId = request.args.get('videoId')

            videoVO = VideoVO()
            videoDAO = VideoDAO()


            videoVO.videoId = videoId

            videoVOList = videoDAO.editVideo(videoVO)
            videoFileName = videoVOList[0].videoFileName

            videoVO.detectionStatus='Detected'
            videoVO.detectionFilePath='../static/adminResources/videos/'
            videoVO.detectionFileName='output_'+videoFileName[:-3]+'avi'

            videoDAO.updateVideo(videoVO)


            loginId=session['session_loginId']

            loginVO=LoginVO()
            loginDAO=LoginDAO()

            loginVO.loginId=loginId
            loginVOList=loginDAO.editLogin(loginVO)


            os.system(r'python yolo-object-detection/yolo_video.py --input project/static/adminResources/videos/'+videoFileName+r' --output project/static/adminResources/videos/output_'+videoFileName[:-3]+'avi'+r' --yolo yolo-object-detection/yolo-coco'+' --username '+loginVOList[0].loginUsername)
            return redirect(url_for('userViewVideo'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
