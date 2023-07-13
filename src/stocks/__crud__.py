from src.database.__conn__ import Session
from src.database.__cart__ import Cart, CartTable
from src.settings.dependency import *

class CartCommands:
    def create(self, session, target):
        try:
            session.add(target)
            session.commit()
        except Exception as e:
            return str(e)
    def read(self, tmpSession, where, id=None, product_id=None):
        if id == None:
            if product_id == None:
                return tmpSession.query(where).all()
            else:
                return tmpSession.query(where).filter_by(product_id=product_id).all()
        elif product_id == None:
            return tmpSession.query(where).filter_by(user_id=id).all()
        else:
            return tmpSession.query(where).filter_by(user_id=id).filter_by(product_id=product_id).first()
    def update(self, tmpSession, where, target):
        # change DB Data
        try:
            tmpSession.query(where).filter_by(user_id=target.user_id).update({
                where.user_id: target.user_id,
                where.product_id: target.product_id,
                where.product_price: target.product_price,
                where.product_count: target.product_count
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