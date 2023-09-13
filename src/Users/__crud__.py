from src.database.__user__ import UserTable, User
from src.settings.dependency import *


class UserCommands:
    def create(self, session, target):
        try:
            session.add(target)
            session.commit()
        except Exception as e:
            return str(e)
    def read(self, tmpSession, where, id=None, password=None):
        if id == None:
            if password == None:
                return tmpSession.query(where).all()
            else:
                return None
        elif password == None:
            return tmpSession.query(where).filter_by(user_id=id).first()
        else:
            return tmpSession.query(where).filter_by(user_id=id).filter_by(user_pw=password).first()
    def update(self, tmpSession, where, target):
        # change DB Data
        try:
            tmpSession.query(where).filter_by(user_id=target.user_id).update({
                where.user_name: target.user_name,
                where.user_id: target.user_id,
                where.user_pw: target.user_pw,
                where.user_email: target.user_email,
                where.user_phone: target.user_phone
            })
            tmpSession.commit()

            return None
        except Exception as e:
            return str(e)
    def delete(self, tmpSession, where, user_id):
        try:
            tmpSession.query(where).filter_by(user_id=user_id).delete()
            tmpSession.commit()
        except Exception as e:
            return str(e)