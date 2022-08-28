from project import app
from flask import render_template, redirect, request, url_for, session
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.controller.LoginController import adminLoginSession
import datetime


@app.route('/user/loadFeedback')
def userLoadFeedback():
    try:
        if adminLoginSession()=='user':
            return render_template('user/addFeedback.html')
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST'])
def userInsertFeedback():
    try:
        if adminLoginSession()=='user':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']
            feedbackDate = datetime.datetime.now().date()
            feedbackTime = datetime.datetime.now().time()
            feedbackFrom_LoginId = session['session_loginId']

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('userViewFeedback'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/viewFeedback')
def userViewFeedback():
    try:
        if adminLoginSession()=='user':
            feedbackVO=FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackFrom_LoginId=session['session_loginId']
            feedbackVOList = feedbackDAO.userViewFeedback(feedbackVO)

            return render_template('user/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewFeedback')
def adminViewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVOList = feedbackDAO.adminViewFeedback()
            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/reviewFeedback')
def adminReviewFeedback():
    try:
        if adminLoginSession()=='admin':
            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.updateFeedback(feedbackVO)

            return redirect(url_for('adminViewFeedback'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/user/deleteFeedback')
def userDeleteFeedback():
    try:
        if adminLoginSession()=='user':
            feedbackId = request.args.get('feedbackId')

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackId = feedbackId
            feedbackDAO.deleteFeedback(feedbackVO)

            return redirect(url_for('userViewFeedback'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
