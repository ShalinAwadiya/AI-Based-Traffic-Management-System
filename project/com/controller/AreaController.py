from project import app
from flask import request, render_template, redirect, url_for
from project.com.dao.AreaDAO import AreaDAO
from project.com.vo.AreaVO import AreaVO
from project.com.controller.LoginController import adminLoginSession


@app.route('/admin/loadArea', methods=['GET'])
def adminLoadArea():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addArea.html')
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewArea', methods=['GET'])
def adminViewArea():
    try:
        if adminLoginSession() == 'admin':
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()
            print('__________', areaVOList)
            return render_template('admin/viewArea.html', areaVOList=areaVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertArea', methods=['POST'])
def adminInsertArea():
    try:
        if adminLoginSession() == 'admin':
            areaName = request.form['areaName']
            areaPincode = request.form['areaPincode']

            areaVO = AreaVO()
            areaDAO = AreaDAO()

            areaVO.areaName = areaName
            areaVO.areaPincode = areaPincode

            areaDAO.insertArea(areaVO)

            return redirect(url_for('adminViewArea'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteArea', methods=['GET'])
def adminDeleteArea():
    try:
        if adminLoginSession() == 'admin':
            areaVO = AreaVO()
            areaDAO = AreaDAO()

            areaId = request.args.get('areaId')

            areaVO.areaId = areaId

            areaDAO.deleteArea(areaVO)

            return redirect(url_for('adminViewArea'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/editArea', methods=['GET'])
def adminEditArea():
    try:
        if adminLoginSession() == 'admin':
            areaVO = AreaVO()
            areaDAO = AreaDAO()

            areaId = request.args.get('areaId')

            areaVO.areaId = areaId

            areaVOList = areaDAO.editArea(areaVO)

            return render_template('admin/editArea.html', areaVOList=areaVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/updateArea', methods=['POST'])
def adminUpdateArea():
    try:
        if adminLoginSession() == 'admin':
            areaId = request.form['areaId']
            areaName = request.form['areaName']
            areaPincode = request.form['areaPincode']

            areaVO = AreaVO()
            areaDAO = AreaDAO()

            areaVO.areaId = areaId
            areaVO.areaName = areaName
            areaVO.areaPincode = areaPincode

            areaDAO.updateArea(areaVO)

            return redirect(url_for('adminViewArea'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
