from project import db
from project.com.vo.AreaVO import AreaVO


class CrossroadVO(db.Model):
    __tablename__ = 'crossroadmaster'
    crossroadId = db.Column('crossroadId', db.Integer, primary_key=True, autoincrement=True)
    crossroadName = db.Column('crossroadName', db.String(100))
    crossroad_AreaId = db.Column('crossroad_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))

    def as_dict(self):
        return {
            'crossroadId': self.crossroadId,
            'crossroadName': self.crossroadName,
            'crossroad_AreaId': self.crossroad_AreaId
        }


db.create_all()
