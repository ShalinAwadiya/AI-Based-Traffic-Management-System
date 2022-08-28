from project import app
from flask import render_template, request, redirect, url_for
from project.com.dao.CameraDAO import CameraDAO
from project.com.vo.CameraVO import CameraVO
from project.com.dao.CrossroadDAO import CrossroadDAO
from project.com.dao.AreaDAO import AreaDAO
from project.com.controller.LoginController import adminLoginSession


@app.route('/admin/loadCamera')
def adminLoadCamera():
    try:
        if adminLoginSession() == 'admin':
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            crossroadDAO = CrossroadDAO()
            crossroadVOList = crossroadDAO.viewCrossroad()

            return render_template('admin/addCamera.html', crossroadVOList=crossroadVOList, areaVOList=areaVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertCamera', methods=['Post'])
def adminInsertCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraCode = request.form['cameraCode']
            camera_AreaId = request.form['camera_AreaId']
            camera_CrossroadId = request.form['camera_CrossroadId']

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()

            cameraVO.cameraCode = cameraCode
            cameraVO.camera_AreaId = camera_AreaId
            cameraVO.camera_CrossroadId = camera_CrossroadId

            cameraDAO.insertCamera(cameraVO)

            return redirect(url_for('adminViewCamera'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewCamera')
def adminViewCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraDAO = CameraDAO()
            cameraVOList = cameraDAO.viewCamera()

            return render_template('admin/viewCamera.html', cameraVOList=cameraVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCamera')
def adminDeleteCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraId = request.args.get('cameraId')

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()

            cameraVO.cameraId = cameraId
            cameraDAO.deleteCamera(cameraVO)

            return redirect(url_for('adminViewCamera'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/editCamera')
def adminEditCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraId = request.args.get('cameraId')

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()

            cameraVO.cameraId = cameraId
            cameraVOList = cameraDAO.editCamera(cameraVO)

            crossroadDAO = CrossroadDAO()
            crossroadVOList = crossroadDAO.viewCrossroad()

            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            return render_template('admin/editCamera.html', cameraVOList=cameraVOList, crossroadVOList=crossroadVOList,
                                   areaVOList=areaVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/updateCamera', methods=["POST"])
def adminUpdateCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraId = request.form['cameraId']
            cameraCode = request.form['cameraCode']
            camera_CrossroadId = request.form['camera_CrossroadId']
            camera_AreaId = request.form['camera_AreaId']

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()

            cameraVO.cameraId = cameraId
            cameraVO.cameraCode = cameraCode
            cameraVO.camera_CrossroadId = camera_CrossroadId
            cameraVO.camera_AreaId = camera_AreaId

            cameraDAO.updateCamera(cameraVO)

            return redirect(url_for('adminViewCamera'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
