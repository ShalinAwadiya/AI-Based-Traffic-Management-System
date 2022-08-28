from project import app
from flask import render_template, redirect, request, url_for
from project.com.vo.DatasetVO import DatasetVO
from project.com.dao.DatasetDAO import DatasetDAO
from werkzeug.utils import secure_filename
import os
import datetime
from project.com.controller.LoginController import adminLoginSession



@app.route('/admin/loadDataset')
def adminLoadDataset():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addDataset.html')
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['POST'])
def adminInsertDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            UPLOAD_FOLDER = 'project/static/adminResources/dataset/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']

            datasetFileName = secure_filename(file.filename)
            datasetFilePath = os.path.join(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(datasetFilePath, datasetFileName))

            datasetVO.datasetFileName = datasetFileName
            datasetVO.datasetFilePath = datasetFilePath.replace('project', '..')
            datasetVO.uploadDate = datetime.datetime.now().date()
            datasetVO.uploadTime = datetime.datetime.now().time()

            datasetDAO.insertDataset(datasetVO)
            return redirect(url_for('adminViewDataset'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset')
def adminViewDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()
            return render_template('admin/viewDataset.html', datasetVOList=datasetVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset')
def adminDeleteDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetId = request.args.get('datasetId')

            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            datasetVO.datasetId = datasetId
            datasetVOList = datasetDAO.deleteDataset(datasetVO)

            datasetFilePath = datasetVOList.datasetFilePath.replace('..', 'project')
            datasetFile = datasetFilePath + datasetVOList.datasetFileName

            os.remove(datasetFile)

            return redirect(url_for('adminViewDataset'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
