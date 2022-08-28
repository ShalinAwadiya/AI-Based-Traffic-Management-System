from project import app
from flask import render_template, redirect
from project.com.controller.LoginController import adminLoginSession


@app.route('/user/viewDetection')
def userViewDetection():
    try:
        if adminLoginSession()=='user':
            return render_template('user/viewDetection.html')
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)




