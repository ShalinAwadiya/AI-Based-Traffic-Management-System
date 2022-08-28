from project import app
from flask import render_template, request, url_for, redirect, session
from project.com.vo.LoginVO import LoginVO
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.VideoVO import VideoVO
from project.com.dao.VideoDAO import VideoDAO
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



@app.route('/')
def adminLoadLogin():
    try:
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard')
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            videoDAO = VideoDAO()
            videoVOList = videoDAO.adminViewVideo()
            return render_template('admin/index.html',videoVOList=videoVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)



@app.route('/user/loadDashboard')
def userLoadDashboard():
    try:
        if adminLoginSession()=='user':
            videoVO=VideoVO()
            videoDAO = VideoDAO()

            videoVO.videoId=session['session_loginId']
            videoVOList = videoDAO.userViewVideo(videoVO)
            return render_template('user/index.html', videoVOList=videoVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)



@app.route('/admin/validateLogin', methods=['POST'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginStatus = 'active'

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        lenLoginDictList = len(loginDictList)
        if lenLoginDictList == 0:
            msg = 'Username or password is incorrect !'
            return render_template('admin/login.html', error=msg)
        else:
            for row in loginDictList:
                loginId = row['loginId']
                loginUsername = row['loginUsername']
                loginRole = row['loginRole']

                session['session_loginId'] = loginId
                session['session_loginUsername'] = loginUsername
                session['session_loginRole'] = loginRole
                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))
                elif loginRole=='user':
                    return redirect(url_for('userLoadDashboard'))

    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:
            if session['session_loginRole'] == 'admin':
                return 'admin'
            elif session['session_loginRole'] == 'user':
                return 'user'
        else:
            return False
    except Exception as ex:
        print(ex)


@app.route('/admin/logoutSession')
def adminLogoutSession():
    try:
        session.clear()
        return redirect(url_for('adminLoadLogin'))
    except Exception as ex:
        print(ex)


@app.route('/admin/forgotPassword', methods=['POST'])
def adminForgotPassword():
    try:
        loginUsername = request.form['loginUsername']

        loginVO=LoginVO()
        loginDAO=LoginDAO()

        loginVO.loginUsername=loginUsername
        loginVOList=loginDAO.editLoginByUsername(loginVO)

        if len(loginVOList)==0:
            msg='The username you have entered does not exist !'
            return render_template('admin/login.html', error=msg)
        else:
            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
            sender = 'aipythonshalin@gmail.com'
            receiver = loginUsername

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = 'PYTHON PASSWORD'
            msg.attach(MIMEText('New Password:'+loginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, 'vnzbkfmgtaubsgut')
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()

            loginVO.loginId=loginVOList[0].loginId
            loginVO.loginPassword=loginPassword

            loginDAO.updateLogin(loginVO)

            msg='A new password has been sent to your email address.'

            return render_template('admin/login.html',error=msg)
    except Exception as ex:
        print(ex)

