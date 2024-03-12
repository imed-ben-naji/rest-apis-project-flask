from src.utils.db import db 
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.schemas import StoreSchema
from src.models.store import StoreModel
from src.services.store_service import StoreService


blp = Blueprint('store', __name__, description='Store operations')

store_service = StoreService()

@blp.route('/store/<int:store_id>')
class Store(MethodView):
        # get all stores
        @blp.response(200, StoreSchema)
        def get(self, store_id):
             return store_service.getStore(store_id)
        # delete a store using its id
        def delete(self, store_id):
            return store_service.deleteStore(store_id)
@blp.route('/store')
class StoreList(MethodView):
        # get all stores
        @blp.response(200, StoreSchema(many=True))
        def get(self):
            return store_service.getStores()
        # Create a store
        @blp.arguments(StoreSchema)
        @blp.response(201, StoreSchema)
        def post(self, store_data):
            return store_service.createStore(store_data)