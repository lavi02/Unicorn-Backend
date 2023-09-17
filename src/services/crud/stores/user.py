from src.database.stores.user import StoreUserTable
from dependency_injector.wiring import inject
from sqlalchemy.orm import Session
# store.store_code is foreign key
class StoreUserCommands:
    @inject
    def create(self, session: Session, target: StoreUserTable):
        try:
            session.add(target)
            return session.commit()
        except Exception as e:
            return str(e)
        
    @inject
    def read(self, session: Session, where: StoreUserTable, store_code=None, user_id=None):
        # store_code, store_status
        try:
            if store_code == None:
                if user_id == None:
                    return session.query(where).all()
                else:
                    return session.query(where).filter_by(user_id=user_id).all()
            elif user_id == None:
                return session.query(where).filter_by(store_code=store_code).first()
            else:
                return session.query(where).filter_by(store_code=store_code).filter_by(user_id=user_id).first()
        except Exception as e:
            return str(e)
        
    @inject
    def update(self, session: Session, where: StoreUserTable, target: StoreUserTable):
        # change DB Data
        try:
            session.query(where).filter_by(store_code=target.store_code).filter_by(user_id=target.user_id).update({
                StoreUserTable.user_role: target.user_role
            })
            session.commit()
            return None
        except Exception as e:
            return str(e)
        
    @inject
    def delete(self, session: Session, where: StoreUserTable, store_code: str, user_id: str):
        try:
            session.query(where).filter_by(store_code=store_code).filter_by(user_id=user_id).delete()
            session.commit()
        except Exception as e:
            return str(e)