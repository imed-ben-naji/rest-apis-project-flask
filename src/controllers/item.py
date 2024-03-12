from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt

from src.utils.db import db
from sqlalchemy.exc import SQLAlchemyError
from src.schemas import ItemSchema, UpdateItemSchema
from src.models.item import ItemModel
from src.services.item_service import ItemService

blp = Blueprint('Items', __name__, description='Item operations')

resource_service = ItemService()

@blp.route('/item/<int:item_id>')
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        return resource_service.getItem(item_id)
    
    @jwt_required()
    def delete(self, item_id):
        return resource_service.deleteItem(item_id)
    
    @blp.arguments(UpdateItemSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        return resource_service.updateItem(item_data, item_id)


@blp.route('/item')
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return resource_service.getItems()
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        return resource_service.createItem(item_data)