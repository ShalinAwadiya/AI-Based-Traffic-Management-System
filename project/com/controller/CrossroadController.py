from project import app
from flask import render_template, request, url_for, redirect
from project.com.dao.CrossroadDAO import CrossroadDAO
from project.com.vo.CrossroadVO import CrossroadVO
from project.com.dao.AreaDAO import AreaDAO
from project.com.controller.LoginController import adminLoginSession


@app.route('/admin/loadCrossroad', methods=['GET'])
def adminLoadCrossroad():
    try:
        if adminLoginSession() == 'admin':
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()
            return render_template('admin/addCrossroad.html', areaVOList=areaVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewCrossroad', methods=['GET'])
def adminViewCrossroad():
    try:
        if adminLoginSession() == 'admin':
            crossroadDAO = CrossroadDAO()
            crossroadVOList = crossroadDAO.viewCrossroad()

            return render_template('admin/viewCrossroad.html', crossroadVOList=crossroadVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertCrossroad', methods=['POST'])
def adminInsertCrossroad():
    try:
        if adminLoginSession() == 'admin':
            crossroad_AreaId = request.form['crossroad_AreaId']
            crossroadName = request.form['crossroadName']

            crossroadVO = CrossroadVO()
            crossroadDAO = CrossroadDAO()

            crossroadVO.crossroad_AreaId = crossroad_AreaId
            crossroadVO.crossroadName = crossroadName

            crossroadDAO.insertCrossroad(crossroadVO)

            return redirect(url_for('adminViewCrossroad'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCrossroad', methods=['GET'])
def adminDeleteCrossroad():
    try:
        if adminLoginSession() == 'admin':
            crossroadId = request.args.get('crossroadId')

            crossroadVO = CrossroadVO()
            crossroadDAO = CrossroadDAO()

            crossroadVO.crossroadId = crossroadId

            crossroadDAO.deleteCrossroad(crossroadVO)

            return redirect(url_for('adminViewCrossroad'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/editCrossroad', methods=['GET'])
def adminEditCrossroad():
    try:
        if adminLoginSession() == 'admin':
            crossroadId = request.args.get('crossroadId')

            crossroadVO = CrossroadVO()
            crossroadDAO = CrossroadDAO()

            crossroadVO.crossroadId = crossroadId
            crossroadVOList = crossroadDAO.editCrossroad(crossroadVO)

            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            return render_template('admin/editCrossroad.html', crossroadVOList=crossroadVOList, areaVOList=areaVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/updateCrossroad', methods=['POST'])
def adminUpdateCrossroad():
    try:
        if adminLoginSession() == 'admin':
            crossroadId = request.form['crossroadId']
            crossroadName = request.form['crossroadName']
            crossroad_AreaId = request.form['crossroad_AreaId']

            crossroadVO = CrossroadVO()
            crossroadDAO = CrossroadDAO()

            crossroadVO.crossroadId = crossroadId
            crossroadVO.crossroadName = crossroadName
            crossroadVO.crossroad_AreaId = crossroad_AreaId

            crossroadDAO.updateCrossroad(crossroadVO)
            return redirect(url_for('adminViewCrossroad'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
