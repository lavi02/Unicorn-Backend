from src.database.__store__ import *

from src.settings.dependency import *
from src.database.__stocks__ import *

# store.store_code is foreign key
class CodeCommands:
    def onlyCommit(self, session):
        try:
            session.commit()
            return None
        except Exception as e:
            return str(e)
    def create(self, session, target):
        try:
            session.add(target)
            session.commit()
        except Exception as e:
            print(e)
            return str(e)
    def read(self, session, where, store_code, table_number=None):
        # store_code, table_code
        if table_number == None:
            return session.query(where).filter_by(store_code=store_code).all()
        return session.query(where).filter_by(store_code=store_code).filter_by(table_number=table_number).all()
    def update(self, session, where, store_code, table_number, target):
        # change DB Data
        try:
            session.query(where).filter_by(store_code=store_code).filter_by(table_number=table_number).update({
                where.table_status: target.table_status
            })
            session.commit()
        except Exception as e:
            return str(e)
