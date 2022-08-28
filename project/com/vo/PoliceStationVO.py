from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.LoginVO import LoginVO


class PoliceStationVO(db.Model):
    __tablename__ = 'policestationmaster'
    policeStationId = db.Column('policeStationId', db.Integer, primary_key=True, autoincrement=True)
    policeStationName = db.Column('policeStationName', db.String(200))
    policeStationAddress = db.Column('policeStationAddress', db.String(200))
    policeStationContact = db.Column('policeStationContact', db.String(15), unique=True)
    policeStation_AreaId = db.Column('policeStation_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    policeStation_LoginId = db.Column('policeStation_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'policeStationId': self.policeStationId,
            'policeStationName': self.policeStationName,
            'policeStationAddress': self.policeStationAddress,
            'policeStationContact': self.policeStationContact,
            'policeStation_AreaId': self.policeStation_AreaId,
            'policeStation_LoginId': self.policeStation_LoginId
        }


db.create_all()
