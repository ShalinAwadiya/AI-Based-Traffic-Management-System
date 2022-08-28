from project import db


class DatasetVO(db.Model):
    __tablename__ = 'datasetmaster'
    datasetId = db.Column('datasetId', db.Integer, primary_key=True, autoincrement=True)
    datasetFileName = db.Column('datasetFileName', db.String(100))
    datasetFilePath = db.Column('datasetFilePath', db.String(100))
    uploadDate = db.Column('uploadDate', db.DATE)
    uploadTime = db.Column('uploadTime', db.TIME)

    def as_dict(self):
        return {
            'datasetId': self.datasetId,
            'datasetFileName': self.datasetFileName,
            'datasetFilePath': self.datasetFilePath,
            'uploadDate': self.uploadDate,
            'uploadTime': self.uploadTime
        }


db.create_all()
