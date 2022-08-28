from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.PoliceStationVO import PoliceStationVO


class PoliceStationDAO:
    def insertPoliceStation(self, policeStationVO):
        db.session.add(policeStationVO)
        db.session.commit()

    def viewPoliceStation(self):
        policeStationList = db.session.query(PoliceStationVO, AreaVO, LoginVO) \
            .join(AreaVO, PoliceStationVO.policeStation_AreaId == AreaVO.areaId) \
            .join(LoginVO, PoliceStationVO.policeStation_LoginId == LoginVO.loginId).all()

        return policeStationList

    def deletePoliceStation(self, policeStationVO):
        policeStationList = PoliceStationVO.query.get(policeStationVO.policeStationId)

        db.session.delete(policeStationList)
        db.session.commit()

        return policeStationList



    def editPoliceStation(self, policeStationVO):
        policeStationList=PoliceStationVO.query.filter_by(policeStationId=policeStationVO.policeStationId).all()

        return policeStationList

    def updatePoliceStation(self, policeStationVO):
        db.session.merge(policeStationVO)
        db.session.commit()
