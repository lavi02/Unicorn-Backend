from src.database.cart import Cart, CartTable
from dependency_injector.wiring import inject
from sqlalchemy.orm import Session

class CartCommands:
    def create(self, session: Session, target: CartTable):
        try:
            session.add(target)
            session.commit()
        except Exception as e:
            return str(e)
        
    def read(self, session: Session, where: CartTable, id=None, product_id=None):
        if id == None:
            if product_id == None:
                return session.query(where).all()
            else:
                return session.query(where).filter_by(product_id=product_id).all()
        elif product_id == None:
            return session.query(where).filter_by(user_id=id).all()
        else:
            return session.query(where).filter_by(user_id=id).filter_by(product_id=product_id).first()
    
    def update(self, session: Session, where: CartTable, target: CartTable):
        # change DB Data
        try:
            session.query(where).filter_by(user_id=target.user_id).filter_by(product_id=target.product_id).update({
                where.product_price: target.product_price,
                where.product_count: target.product_count
            })
            session.commit()
            return None
        except Exception as e:
            return str(e)
   
    def delete(self, session: Session, where: CartTable, user_id: str, product_id: str):
        try:
            session.query(where).filter_by(user_id=user_id).filter_by(product_id=product_id).delete()
            session.commit()
        except Exception as e:
            return str(e)