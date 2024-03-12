from src.utils.db import db 
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_smorest import abort
from src.models.store import StoreModel


class StoreService():
    def getStore(self, store_id):
            store = StoreModel.query.get_or_404(store_id)
            return store 
    
        # delete a store using its id
    def deleteStore(self, store_id):
            store = StoreModel.query.get_or_404(store_id)
            db.session.delete(store)
            db.session.commit()
            return {'message': 'Store deleted successfully.'}

    def getStores(self):
        return StoreModel.query.all()
    
    def createStore(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(500, message='A store with the same name already exists.')
        except SQLAlchemyError:
            abort(500, message='An error occurred while creating the store.')
        return store