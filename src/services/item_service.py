from flask_smorest import abort
from flask_jwt_extended import get_jwt

from src.utils.db import db
from sqlalchemy.exc import SQLAlchemyError
from src.models.item import ItemModel

class ItemService():
    def getItem(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    def deleteItem(self, item_id):
        # jwt = get_jwt()
        # if not jwt.get('is_admin'):
        #     abort(401, message='You do not have the permission to delete this item.')
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted successfully.'}
    
    def updateItem(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        print(item)
        if item:
            item.name = item_data['name']
            item.price = item_data['price']
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        return item
    
    def getItems(self):
        return ItemModel.query.all()

    def createItem(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500, 
                message='An error occurred while creating the item.--'+str(e)
            )              
        
        return item