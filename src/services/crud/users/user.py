from src.database.users.user import UserTable
from dependency_injector.wiring import inject
from sqlalchemy.orm import Session

class UserCommands:   
    @inject
    def create(self, session: Session, target: UserTable):
        try:
            session.add(target)
            return session.commit()
        except Exception as e:
            return str(e)
    
    @inject
    def read(self, where: UserTable, session: Session, id=None, password=None):
        try:
            if id == None:
                if password == None:
                    return session.query(where).all()
                else:
                    return None
            elif password == None:
                return session.query(where).filter_by(user_id=id).first()
            else:
                return session.query(where).filter_by(user_id=id).filter_by(user_pw=password).first()
        except Exception as e:
            return str(e)
            
    @inject
    def update(self, session: Session, where: UserTable, target: UserTable):
        try:
            session.query(where).filter_by(user_id=target.user_id).update({
                UserTable.user_name: target.user_name,
                UserTable.user_pw: target.user_pw,
                UserTable.user_email: target.user_email,
                UserTable.user_type: target.user_type,
                UserTable.user_phone: target.user_phone,
                UserTable.is_valid: target.is_valid
            })
            session.commit()
            return None
        except Exception as e:
            return str(e)
            
    @inject
    def delete(self, session: Session, where: UserTable, user_id: str):
        try:
            session.query(where).filter_by(user_id=user_id).delete()
            session.commit()
        except Exception as e:
            return str(e)
