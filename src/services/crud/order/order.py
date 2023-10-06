from src.database.orders.order import Order, OrderTable
from dependency_injector.wiring import inject
from sqlalchemy.orm import Session


class OrderCommands:
    def create(self, session: Session, target: OrderTable):
        try:
            session.add(target)
            session.commit()
        except Exception as e:
            return str(e)

    def readTableOrder(self, session: Session, where: OrderTable, store_code: str, table_number: str, status: bool):
        if status == False:
            return session.query(where).filter_by(store_code=store_code).filter_by(table_number=table_number).all()
        else:
            return session.query(where).filter_by(store_code=store_code).filter_by(table_number=table_number).filter_by(status=status).all()
        
    def read(self, session: Session, where: OrderTable, product_status=None,
            id=None, product_id=None, store_cdoe=None):
        if id == None: # 전체 사용자
            if product_id == None: # 전체 상품
                return session.query(where).all()
            else: # 특정 상품
                if store_cdoe == None: # 전체 매장
                    return session.query(where).filter_by(product_id=product_id).all()
                else: # 특정 매장
                    return session.query(where).filter_by(product_id=product_id).filter_by(store_code=store_cdoe).all()
        elif product_id == None: # 특정 사용자, 전체 상품
            if store_cdoe == None: # 전체 매장
                return session.query(where).filter_by(user_id=id).all()
            else: # 특정 매장
                return session.query(where).filter_by(user_id=id).filter_by(store_code=store_cdoe).all()
        else:
            if store_cdoe == None: # 전체 매장
                return session.query(where).filter_by(user_id=id).filter_by(product_id=product_id).all()
            else: # 특정 매장
                return session.query(where).filter_by(user_id=id).filter_by(product_id=product_id).filter_by(store_code=store_cdoe).all()
    
    def update(self, session: Session, where: OrderTable, target: OrderTable):
        # change DB Data
        try:
            session.query(where).filter_by(user_id=target.user_id).update({
                where.user_id: target.user_id,
                where.store_code: target.store_code,
                where.table_number: target.table_number,
                where.product_id: target.product_id,
                where.product_price: target.product_price,
                where.product_count: target.product_count,
                where.product_option: target.product_option,
                where.product_status: target.product_status
            })
            session.commit()

            return None
        except Exception as e:
            return str(e)
        
    def updateStatus(self, session: Session, where: OrderTable, user_id, store_code, product_id, status: bool):
        # change DB Data
        try:
            session.query(where).filter_by(user_id=user_id).filter_by(store_code=store_code).filter_by(product_id=product_id).update({
                where.product_status: status
            })
            session.commit()

            return None
        except Exception as e:
            return str(e)
        
    def delete(self, session: Session, where: OrderTable, user_id, product_id):
        try:
            session.query(where).filter_by(user_id=user_id).filter_by(product_id=product_id).delete()
            session.commit()
        except Exception as e:
            return str(e)