from src.settings.dependency import *
from src.database.__stocks__ import *

# store.store_code is foreign key
class StocksCommands:
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
    def readStoreStocks(self, tmpSession, where, store_code, stock_id=None):
        # store_code, stock_id
        if stock_id == None:
            return tmpSession.query(where).filter_by(store_code=store_code).all()
        else:
            return tmpSession.query(where).filter_by(store_code=store_code).filter_by(stock_id=stock_id).all()
        
    def readStore(self, tmpSession, where, store_code=None, store_status=None):
        # store_code, store_status
        if store_code == None:
            if store_status == None:
                return tmpSession.query(where).all()
            else:
                return tmpSession.query(where).filter_by(store_status=store_status).all()
        else:
            if store_status == None:
                return tmpSession.query(where).filter_by(store_code=store_code).all()
            else:
                return tmpSession.query(where).filter_by(store_code=store_code).filter_by(store_status=store_status).all()
    
    def readStoreUsers(self, tmpSession, where, store_code, user_id=None):
        # store_code, user_id
        # store_code is foreign key
        if user_id == None:
            return tmpSession.query(where).filter_by(store_code=store_code).all()
        else:
            return tmpSession.query(where).filter_by(store_code=store_code).filter_by(user_id=user_id).all()
        
    def updateStoreStocks(self, tmpSession, where, target):
        # change DB Data
        try:
            tmpSession.query(where).filter_by(store_code=target.store_code).filter_by(stock_id=target.stock_id).update({
                where.store_code: target.store_code,
                where.stock_id: target.stock_id,
                where.stock_name: target.stock_name,
                where.stock_price: target.stock_price,
                where.stock_description: target.stock_description,
                where.stock_option: target.stock_option,
                where.stock_category: target.stock_category
            })

            tmpSession.commit()

            return None
        except Exception as e:
            return str(e)
        
    def updateStoreStocksStatus(self, tmpSession, where, status, store_code, stock_id):
        # change DB Data
        try:
            tmpSession.query(where).filter_by(store_code=store_code).filter_by(stock_id=stock_id).update({
                where.stock_status: status
            })

            tmpSession.commit()

            return None
        except Exception as e:
            return str(e)
        
    def updateStoreInfo(self, tmpSession, where, target):
        # change DB Data
        try:
            tmpSession.query(where).filter_by(store_code=target.store_code).update({
                where.store_code: target.store_code,
                where.store_name: target.store_name,
                where.store_status: target.store_status,
            })

            tmpSession.commit()

            return None
        except Exception as e:
            print(e)
            return str(e)
    def updateStoreUserInfo(self, tmpSession, where, target):
        # change DB Data
        try:
            tmpSession.query(where).filter_by(store_code=target.store_code).filter_by(user_id=target.user_id).update({
                where.store_code: target.store_code,
                where.user_id: target.user_id,
                where.user_pw: target.user_pw,
                where.user_email: target.user_email,
                where.user_phone: target.user_phone,
            })

            tmpSession.commit()

            return None
        except Exception as e:
            return str(e)
        
    
    def deleteStocks(self, tmpSession, where, store_code, stock_id):
        try:
            tmpSession.query(StockImages).filter_by(stock_id=stock_id).delete()
            tmpSession.query(where).filter_by(store_code=store_code).filter_by(stock_id=stock_id).delete()
            tmpSession.commit()
        except Exception as e:
            return str(e)
        
    def deleteStocksImages(self, tmpSession, where, store_code, stock_id, urls):
        try:
            stock = tmpSession.query(where).filter_by(stock_id=stock_id).first()
            if stock:
                image = tmpSession.query(StockImages).filter_by(image=urls).first()
                if image:
                    tmpSession.delete(image)
                tmpSession.commit()
        except Exception as e:
            return str(e)