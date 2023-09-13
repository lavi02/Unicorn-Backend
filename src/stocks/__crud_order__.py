from src.database.__conn__ import Session
from src.database.__order__ import Order, OrderTable
from src.settings.dependency import *

class OrderCommands:
    def create(self, session, target):
        try:
            session.add(target)
            session.commit()
        except Exception as e:
            return str(e)
    def readTableOrder(self, tmpSession, where, store_code, table_number, status: bool):
        if status == False:
            return tmpSession.query(where).filter_by(store_code=store_code).filter_by(table_number=table_number).all()
        else:
            return tmpSession.query(where).filter_by(store_code=store_code).filter_by(table_number=table_number).filter_by(status=status).all()
        
    def read(self, tmpSession, where, product_status=None,
            id=None, product_id=None, store_cdoe=None):
        if id == None: # 전체 사용자
            if product_id == None: # 전체 상품
                return tmpSession.query(where).all()
            else: # 특정 상품
                if store_cdoe == None: # 전체 매장
                    return tmpSession.query(where).filter_by(product_id=product_id).all()
                else: # 특정 매장
                    return tmpSession.query(where).filter_by(product_id=product_id).filter_by(store_code=store_cdoe).all()
        elif product_id == None: # 특정 사용자, 전체 상품
            if store_cdoe == None: # 전체 매장
                return tmpSession.query(where).filter_by(user_id=id).all()
            else: # 특정 매장
                return tmpSession.query(where).filter_by(user_id=id).filter_by(store_code=store_cdoe).all()
        else:
            if store_cdoe == None: # 전체 매장
                return tmpSession.query(where).filter_by(user_id=id).filter_by(product_id=product_id).all()
            else: # 특정 매장
                return tmpSession.query(where).filter_by(user_id=id).filter_by(product_id=product_id).filter_by(store_code=store_cdoe).all()
    def update(self, tmpSession, where, target):
        # change DB Data
        try:
            tmpSession.query(where).filter_by(user_id=target.user_id).update({
                where.user_id: target.user_id,
                where.store_code: target.store_code,
                where.table_number: target.table_number,
                where.product_id: target.product_id,
                where.product_price: target.product_price,
                where.product_count: target.product_count,
                where.product_option: target.product_option,
                where.product_status: target.product_status
            })
            tmpSession.commit()

            return None
        except Exception as e:
            return str(e)
    def delete(self, tmpSession, where, user_id, product_id):
        try:
            tmpSession.query(where).filter_by(user_id=user_id).filter_by(product_id=product_id).delete()
            tmpSession.commit()
        except Exception as e:
            return str(e)