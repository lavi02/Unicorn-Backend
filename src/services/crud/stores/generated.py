from src.database.stores.tables.generated import GeneratedTable
from dependency_injector.wiring import inject
from sqlalchemy.orm import Session

# store.store_code is foreign key
class TableCommands:
    @inject
    def create(self, session: Session, target: GeneratedTable):
        try:
            session.add(target)
            return session.commit()
        except Exception as e:
            return str(e)
        
    @inject
    def read(self, session: Session, where: GeneratedTable, store_code=None, table_number=None):
        # store_code, store_status
        try:
            if store_code == None:
                if table_number == None:
                    return session.query(where).all()
                else:
                    return session.query(where).filter_by(table_number=table_number).all()
            elif table_number == None:
                return session.query(where).filter_by(store_code=store_code).first()
            else:
                return session.query(where).filter_by(store_code=store_code).filter_by(table_number=table_number).first()
        except Exception as e:
            return str(e)
        
    @inject
    def update(self, session: Session, where: GeneratedTable, target: GeneratedTable):
        # change DB Data
        try:
            session.query(where).filter_by(store_code=target.store_code).filter_by(table_number=target.table_number).update({
                GeneratedTable.table_status: target.table_status
            })
            session.commit()
            return None
        except Exception as e:
            return str(e)
        
    @inject
    def delete(self, session: Session, where: GeneratedTable, store_code: str, table_number: str):
        try:
            session.query(where).filter_by(store_code=store_code).filter_by(table_number=table_number).delete()
            session.commit()
        except Exception as e:
            return str(e)