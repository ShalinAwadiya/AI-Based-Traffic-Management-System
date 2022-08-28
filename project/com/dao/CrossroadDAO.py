from project import db
from project.com.vo.CrossroadVO import CrossroadVO
from project.com.vo.AreaVO import AreaVO


class CrossroadDAO:
    def viewCrossroad(self):
        crossroadList = db.session.query(CrossroadVO, AreaVO).join(AreaVO,
                                                                   CrossroadVO.crossroad_AreaId == AreaVO.areaId).all()

        return crossroadList

    def insertCrossroad(self, crossroadVO):
        db.session.add(crossroadVO)
        db.session.commit()

    def deleteCrossroad(self, crossroadVO):
        crossroadList = CrossroadVO.query.get(crossroadVO.crossroadId)
        db.session.delete(crossroadList)
        db.session.commit()

    def editCrossroad(self, crossroadVO):
        crossroadList = CrossroadVO.query.filter_by(crossroadId=crossroadVO.crossroadId)

        return crossroadList

    def updateCrossroad(self, crossroadVO):
        db.session.merge(crossroadVO)
        db.session.commit()
