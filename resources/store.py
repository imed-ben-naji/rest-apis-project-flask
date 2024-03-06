from db import db 
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models.store import StoreModel


blp = Blueprint('store', __name__, description='Store operations')

@blp.route('/store/<int:store_id>')
class Store(MethodView):
        # get all stores
        @blp.response(200, StoreSchema)
        def get(self, store_id):
            store = StoreModel.query.get_or_404(store_id)
            return store 
    
        # delete a store using its id
        def delete(self, store_id):
            store = StoreModel.query.get_or_404(store_id)
            db.session.delete(store)
            db.session.commit()
            return {'message': 'Store deleted successfully.'}

@blp.route('/store')
class StoreList(MethodView):
        # get all stores
        @blp.response(200, StoreSchema(many=True))
        def get(self):
            return StoreModel.query.all()

        # Create a store
        @blp.arguments(StoreSchema)
        @blp.response(201, StoreSchema)
        def post(self, store_data):
            store = StoreModel(**store_data)
            try:
                db.session.add(store)
                db.session.commit()
            except IntegrityError:
                abort(500, message='A store with the same name already exists.')
            except SQLAlchemyError:
                abort(500, message='An error occurred while creating the store.')
            return store