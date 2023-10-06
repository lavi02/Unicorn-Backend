from src.database.stocks.stock import Stocks, StocksTable
from src.database.stocks.images import StockImages
from dependency_injector.wiring import inject
from sqlalchemy.orm import Session


# store.store_code is foreign key
class StocksCommands:
    def onlyCommit(self, session: Session):
        try:
            session.commit()
            return None
        except Exception as e:
            return str(e)
        
    def create(self, session: Session, target: StocksTable):
        try:
            session.add(target)
            session.commit()
        except Exception as e:
            print(e)
            return str(e)

    def readStoreStocks(self, session: Session, where: StocksTable, store_code, stock_id=None):
        # store_code, stock_id
        if stock_id == None:
            return session.query(where).filter_by(store_code=store_code).all()
        else:
            return session.query(where).filter_by(store_code=store_code).filter_by(stock_id=stock_id).all()
        
    def readStore(self, session: Session, where: StocksTable, store_code=None, store_status=None):
        # store_code, store_status
        if store_code == None:
            if store_status == None:
                return session.query(where).all()
            else:
                return session.query(where).filter_by(store_status=store_status).all()
        else:
            if store_status == None:
                return session.query(where).filter_by(store_code=store_code).all()
            else:
                return session.query(where).filter_by(store_code=store_code).filter_by(store_status=store_status).all()
    
    def readStoreUsers(self, session: Session, where: StocksTable, store_code, user_id=None):
        # store_code, user_id
        # store_code is foreign key
        if user_id == None:
            return session.query(where).filter_by(store_code=store_code).all()
        else:
            return session.query(where).filter_by(store_code=store_code).filter_by(user_id=user_id).all()
        
    def updateStoreStocks(self, session: Session, where: StocksTable, target:StocksTable):
        # change DB Data
        try:
            session.query(where).filter_by(store_code=target.store_code).filter_by(stock_id=target.stock_id).update({
                where.store_code: target.store_code,
                where.stock_id: target.stock_id,
                where.stock_name: target.stock_name,
                where.stock_price: target.stock_price,
                where.stock_description: target.stock_description,
                where.stock_option: target.stock_option,
                where.stock_category: target.stock_category
            })

            session.commit()

            return None
        except Exception as e:
            return str(e)
        
    def updateStoreStocksStatus(self, session: Session, where: StocksTable, status, store_code, stock_id):
        # change DB Data
        try:
            session.query(where).filter_by(store_code=store_code).filter_by(stock_id=stock_id).update({
                where.stock_status: status
            })

            session.commit()

            return None
        except Exception as e:
            return str(e)
        
    def updateStoreInfo(self, session: Session, where, target):
        # change DB Data
        try:
            session.query(where).filter_by(store_code=target.store_code).update({
                where.store_code: target.store_code,
                where.store_name: target.store_name,
                where.store_status: target.store_status,
            })

            session.commit()

            return None
        except Exception as e:
            print(e)
            return str(e)
        
    def updateStoreUserInfo(self, session: Session, where, target):
        # change DB Data
        try:
            session.query(where).filter_by(store_code=target.store_code).filter_by(user_id=target.user_id).update({
                where.store_code: target.store_code,
                where.user_id: target.user_id,
                where.user_pw: target.user_pw,
                where.user_email: target.user_email,
                where.user_phone: target.user_phone,
            })

            session.commit()

            return None
        except Exception as e:
            return str(e)
    
    def deleteStocks(self, session: Session, where, store_code, stock_id):
        try:
            session.query(StockImages).filter_by(stock_id=stock_id).delete()
            session.query(where).filter_by(store_code=store_code).filter_by(stock_id=stock_id).delete()
            session.commit()
        except Exception as e:
            return str(e)
        
    def deleteStocksImages(self, session: Session, where, store_code, stock_id, urls):
        try:
            stock = session.query(where).filter_by(stock_id=stock_id).first()
            if stock:
                image = session.query(StockImages).filter_by(image=urls).first()
                if image:
                    session.delete(image)
                session.commit()
        except Exception as e:
            return str(e)

    def updateStoreTotalPrice(self, session: Session, where, store_code, total_price):
        try:
            # 기존 total_price에 total_price를 더함
            session.query(where).filter_by(store_code=store_code).update({
            'total_price': where.total_price + total_price
        }, synchronize_session=False)
            session.commit()
        except Exception as e:
            return str(e)