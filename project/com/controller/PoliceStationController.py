from project import app
from flask import render_template, request, url_for, redirect
from project.com.vo.PoliceStationVO import PoliceStationVO
from project.com.dao.PoliceStationDAO import PoliceStationDAO
from project.com.dao.AreaDAO import AreaDAO
from project.com.vo.LoginVO import LoginVO
from project.com.dao.LoginDAO import LoginDAO
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from project.com.controller.LoginController import adminLoginSession


@app.route('/admin/loadPoliceStation')
def adminLoadPoliceStation():
    try:
        if adminLoginSession() == 'admin':
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()
            return render_template('admin/addPoliceStation.html', areaVOList=areaVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertPoliceStation', methods=['POST'])
def adminInsertPoliceStation():
    try:
        if adminLoginSession() == 'admin':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            policeStationVO = PoliceStationVO()
            policeStationDAO = PoliceStationDAO()

            loginUsername = request.form['loginUsername']

            policeStationName = request.form['policeStationName']
            policeStationAddress = request.form['policeStationAddress']
            policeStationContact = request.form['policeStationContact']
            policeStation_AreaId = request.form['policeStation_AreaId']

            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
            sender = 'aipythonshalin@gmail.com'
            receiver = loginUsername

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = 'PYTHON PASSWORD'
            msg.attach(MIMEText(loginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, 'vnzbkfmgtaubsgut')
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()

            loginVO.loginUsername = loginUsername
            loginVO.loginPassword = loginPassword
            loginVO.loginRole = 'user'
            loginVO.loginStatus = 'active'

            loginDAO.insertLogin(loginVO)

            policeStationVO.policeStationName = policeStationName
            policeStationVO.policeStationAddress = policeStationAddress
            policeStationVO.policeStationContact = policeStationContact
            policeStationVO.policeStation_AreaId = policeStation_AreaId
            policeStationVO.policeStation_LoginId = loginVO.loginId

            policeStationDAO.insertPoliceStation(policeStationVO)

            return redirect(url_for('adminViewPoliceStation'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewPoliceStation')
def adminViewPoliceStation():
    try:
        if adminLoginSession() == 'admin':
            policeStationDAO = PoliceStationDAO()
            policeStationVOList = policeStationDAO.viewPoliceStation()
            return render_template('admin/viewPoliceStation.html', policeStationVOList=policeStationVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/deletePoliceStation')
def adminDeletePoliceStation():
    try:
        if adminLoginSession() == 'admin':
            policeStationId = request.args.get('policeStationId')

            policeStationVO = PoliceStationVO()
            policeStationDAO = PoliceStationDAO()

            policeStationVO.policeStationId = policeStationId
            policeStationVOList = policeStationDAO.deletePoliceStation(policeStationVO)

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginId = policeStationVOList.policeStation_LoginId
            loginDAO.deleteLogin(loginVO)

            return redirect(url_for('adminViewPoliceStation'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/editPoliceStation')
def adminEditPoliceStation():
    try:
        if adminLoginSession() == 'admin':
            policeStationId = request.args.get('policeStationId')

            policeStationVO = PoliceStationVO()
            policeStationDAO = PoliceStationDAO()

            policeStationVO.policeStationId = policeStationId
            policeStationVOList = policeStationDAO.editPoliceStation(policeStationVO)

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginId = policeStationVOList[0].policeStation_LoginId
            loginVOList = loginDAO.editLogin(loginVO)

            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            return render_template('admin/editPoliceStation.html', policeStationVOList=policeStationVOList,
                                   loginVOList=loginVOList, areaVOList=areaVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/updatePoliceStation', methods=['post'])
def adminUpdatePoliceStation():
    try:
        if adminLoginSession() == 'admin':
            policeStationId = request.form['policeStationId']
            policeStationName = request.form['policeStationName']
            policeStation_AreaId = request.form['policeStation_AreaId']
            policeStationAddress = request.form['policeStationAddress']
            policeStationContact = request.form['policeStationContact']
            policeStation_LoginId = request.form['policeStation_LoginId']

            loginUsername = request.form['loginUsername']

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginId = policeStation_LoginId
            loginVOList = loginDAO.editLogin(loginVO)

            if loginUsername == loginVOList[0].loginUsername:
                pass

            else:

                loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
                sender = 'aipythonshalin@gmail.com'
                receiver = loginUsername

                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = 'PYTHON PASSWORD'
                msg.attach(MIMEText(loginPassword, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender, 'vnzbkfmgtaubsgut')
                text = msg.as_string()
                server.sendmail(sender, receiver, text)
                server.quit()

                loginVO.loginUsername = loginUsername
                loginVO.loginPassword = loginPassword

                loginDAO.updateLogin(loginVO)

            policeStationVO = PoliceStationVO()
            policeStationDAO = PoliceStationDAO()

            policeStationVO.policeStationId = policeStationId
            policeStationVO.policeStationName = policeStationName
            policeStationVO.policeStation_AreaId = policeStation_AreaId
            policeStationVO.policeStationAddress = policeStationAddress
            policeStationVO.policeStationContact = policeStationContact
            policeStationVO.policeStation_LoginId = policeStation_LoginId

            policeStationDAO.updatePoliceStation(policeStationVO)

            return redirect(url_for('adminViewPoliceStation'))

        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
