from flask import abort, request

from sqlalchemy.exc import SQLAlchemyError
from src.models.item import ItemModel
from src.models.store import StoreModel
from src.models.tag import TagModel
from src.utils.db import db

class TagService():
    def getTag(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    def getTagsInStore(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    def createTag(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag
    
    def linkTagToItem(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)
        if item.store_id != tag.store_id:
            abort(400, message="Make sure item and tag belong to the same store before linking.")
        
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="An error occurred while adding the tag to the item.")
        return tag
    
    def removeTagFromItem(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="An error occurred while removing the tag from the item.")
        
        return {'message': 'Tag removed from item successfully.', 'tag': tag.name, 'item': item.name}
    
    def deleteTag(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {'message': 'Tag deleted successfully.'}
        abort(400, message='Could not delete the tag. Make sure no item is tagged with it, then try again.')
    