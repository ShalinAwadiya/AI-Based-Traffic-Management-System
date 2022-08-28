from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def insertLogin(self, loginVO):
        db.session.add(loginVO)
        db.session.commit()

    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername, loginPassword=loginVO.loginPassword,loginStatus=loginVO.loginStatus).all()

        return loginList

    def deleteLogin(self,loginVO):
        loginList=LoginVO.query.get(loginVO.loginId)
        db.session.delete(loginList)
        db.session.commit()

    def editLogin(self,loginVO):
        loginList=LoginVO.query.filter_by(loginId=loginVO.loginId).all()

        return loginList

    def editLoginByUsername(self,loginVO):
        loginList=LoginVO.query.filter_by(loginUsername=loginVO.loginUsername).all()

        return loginList

    def updateLogin(self,loginVO):
        db.session.merge(loginVO)
        db.session.commit()

