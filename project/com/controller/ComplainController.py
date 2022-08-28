from project import app
from flask import render_template, request, url_for, redirect, session
from project.com.vo.ComplainVO import ComplainVO
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.controller.LoginController import adminLoginSession
from werkzeug.utils import secure_filename
import os
import datetime


@app.route('/user/loadComplain')
def userLoadComplain():
    try:
        if adminLoginSession()=='user':
            return render_template('user/addComplain.html')
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession()=='user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']

            UPLOAD_FOLDER = 'project/static/adminResources/complainImages/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']
            complainFileName = secure_filename(file.filename)
            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(complainFilePath, complainFileName))

            complainDate = datetime.datetime.now().date()
            complainTime = datetime.datetime.now().time()
            complainStatus = 'Pending'

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainStatus = complainStatus
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath.replace('project', '..')
            complainVO.complainFrom_LoginId = session['session_loginId']

            complainDAO.insertComplain(complainVO)

            return redirect(url_for('userViewComplain'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain')
def userViewComplain():
    try:
        if adminLoginSession()=='user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainVO.complainFrom_LoginId = session['session_loginId']
            complainVOList = complainDAO.userViewComplain(complainVO)
            return render_template('user/viewComplain.html', complainVOList=complainVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewComplain')
def adminViewComplain():
    try:
        if adminLoginSession() == 'admin':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainStatus = 'Pending'
            complainVOList = complainDAO.adminViewComplain(complainVO)

            return render_template('admin/viewComplain.html', complainVOList=complainVOList)

        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply')
def adminLoadComplainReply():
    try:
        if adminLoginSession() == 'admin':
            complainId = request.args.get('complainId')
            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplainReply():
    try:
        if adminLoginSession()=='admin':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']

            UPLOAD_FOLDER = 'project/static/adminResources/complainImages/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']
            replyFileName = secure_filename(file.filename)
            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(replyFilePath, replyFileName))

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace('project', '..')
            complainVO.replyDate = datetime.datetime.now().date()
            complainVO.replyTime = datetime.datetime.now().time()

            complainVO.complainStatus = 'Replied'
            complainVO.complainTo_LoginId = session['session_loginId']

            complainDAO.updateComplain(complainVO)

            return redirect(url_for('adminViewComplain'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/viewComplainReply')
def userViewComplainReply():
    try:
        if adminLoginSession()=='user':
            complainId = request.args.get('complainId')

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainId = complainId
            complainVOList = complainDAO.editComplain(complainVO)

            return render_template('user/viewComplainReply.html', complainVOList=complainVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain')
def userDeleteComplain():
    try:
        if adminLoginSession()=='user':
            complainId = request.args.get('complainId')

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainId = complainId
            complainVOList = complainDAO.deleteComplain(complainVO)

            complainFilePath = complainVOList.complainFilePath.replace('..', 'project')
            complainFile = complainFilePath + complainVOList.complainFileName
            os.remove(complainFile)

            if complainVOList.complainStatus == 'Replied':
                replyFilePath = complainVOList.replyFilePath.replace('..', 'project')
                replyFile = replyFilePath + complainVOList.replyFileName
                os.remove(replyFile)

            return redirect(url_for('userViewComplain'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
