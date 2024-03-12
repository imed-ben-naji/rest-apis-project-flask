from flask.views import MethodView
from flask_smorest import Blueprint

from src.schemas import TagSchema
from src.services.tag_service import TagService

blp = Blueprint('tags', __name__, description='Tag operations')

tag_service = TagService()

@blp.route('/store/<int:store_id>/tag')
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        return tag_service.getTagsInStore(store_id)
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):            
        return tag_service.createTag(tag_data, store_id)
    
@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagsToItem(MethodView):
    @blp.response(200, TagSchema)
    def put(self, item_id, tag_id):
        return tag_service.linkTagToItem(item_id, tag_id)
    
    def delete(self, item_id, tag_id):
        return tag_service.removeTagFromItem(item_id, tag_id)

@blp.route('/tag/<int:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        return tag_service.getTag(tag_id)
    
    @blp.response(
        201,
        description="Delete a tag if no item is tagged with it.",
        example={'message': 'Tag deleted successfully.'}
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(400, description="Returned if the tag is assigned to one or more items. In this case, the tag cannot be deleted.")
    def delete(self, tag_id):
        return tag_service.deleteTag(tag_id)