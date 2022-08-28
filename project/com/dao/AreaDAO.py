from project import db
from project.com.vo.AreaVO import AreaVO


class AreaDAO:
    def viewArea(self):
        areaList = AreaVO.query.all()

        return areaList

    def insertArea(self, areaVO):
        db.session.add(areaVO)
        db.session.commit()

    def deleteArea(self, areaVO):
        areaList = AreaVO.query.get(areaVO.areaId)
        db.session.delete(areaList)
        db.session.commit()

    def editArea(self, areaVO):
        areaList = AreaVO.query.filter_by(areaId=areaVO.areaId).all()

        return areaList

    def updateArea(self, areaVO):
        db.session.merge(areaVO)
        db.session.commit()
