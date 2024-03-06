import json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required,create_refresh_token, get_jwt_identity
from marshmallow import Schema
from passlib.hash import pbkdf2_sha256
from blocklist import BLOCKLIST

from db import db
from models.user import UserModel
from schemas import UserSchema

blp = Blueprint('Users', 'users', description='Operations on users')


@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data['username']).first():
            abort(400, message="User already exists.")
        user = UserModel(**user_data)
        user.password = pbkdf2_sha256.hash(user.password)
        
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully.'}

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema())
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data['username']).first()
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        abort(401, message="Invalid username or password.")

@blp.route('/refresh')
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # add the refreshed token to the blocklist to prevent it from being used again
        # jti = get_jwt()['jti']
        # BLOCKLIST.add(jti)
        return {'access_token': new_token}

@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {'message': 'Successfully logged out.'}

@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            abort(500, message="An error occurred while deleting the user.")
        return {'message': 'User deleted successfully.'}