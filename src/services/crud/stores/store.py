from src.database.stores.store import StoreTable
from dependency_injector.wiring import inject
from sqlalchemy.orm import Session

# store.store_code is foreign key


class StoreCommands:
    @inject
    def create(self, session: Session, target: StoreTable):
        try:
            session.add(target)
            return session.commit()
        except Exception as e:
            return str(e)

    @inject
    def read(self, session: Session, where: StoreTable, store_code=None, store_status=None):
        # store_code, store_status
        try:
            if store_code == None:
                if store_status == None:
                    return session.query(where).all()
                else:
                    return session.query(where).filter_by(store_status=store_status).all()
            elif store_status == None:
                return session.query(where).filter_by(store_code=store_code).first()
            else:
                return session.query(where).filter_by(store_code=store_code).filter_by(store_status=store_status).first()
        except Exception as e:
            return str(e)

    @inject
    def update(self, tmpSession, where: StoreTable, target: StoreTable):
        # change DB Data
        try:
            tmpSession.query(where).filter_by(store_code=target.store_code).update({
                StoreTable.store_name: target.store_name if target.store_name != None else StoreTable.store_name,
                StoreTable.store_status: target.store_status,
            })
            tmpSession.commit()
            return None
        except Exception as e:
            return str(e)

    @inject
    def delete(self, session: Session, where: StoreTable, store_code: str):
        try:
            session.query(where).filter_by(store_code=store_code).delete()
            session.commit()
        except Exception as e:
            return str(e)
