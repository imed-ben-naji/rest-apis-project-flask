from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

import src.services.user_service as UserService


from src.schemas import UserSchema

blp = Blueprint('Users', 'users', description='Operations on users')


@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        return UserService.create_user(user_data)

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema())
    def post(self, user_data):
        return UserService.login_user(user_data)

@blp.route('/refresh')
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        return UserService.refresh_user()

@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        return UserService.logout_user()

@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return UserService.get_user(user_id)
    
    def delete(self, user_id):
        return UserService.delete_user(user_id)