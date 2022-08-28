from project import db
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO


class FeedbackDAO:
    def insertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)
        db.session.commit()

    def userViewFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.filter_by(feedbackFrom_LoginId=feedbackVO.feedbackFrom_LoginId).all()
        return feedbackList

    def adminViewFeedback(self):
        feedbackList = db.session.query(FeedbackVO, LoginVO) \
            .join(LoginVO, FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId).all()
        return feedbackList

    def deleteFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.get(feedbackVO.feedbackId)
        db.session.delete(feedbackList)
        db.session.commit()

    def editFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.filter_by(feedbackId=feedbackVO.feedbackId).all()

        return feedbackList

    def updateFeedback(self, feedbackVO):
        db.session.merge(feedbackVO)
        db.session.commit()
