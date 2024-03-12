from flask import json
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.utils.oidc import oidc
from src.utils.db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint('OIDC', __name__, description='OIDC operations')

@blp.route('/oidc')
class OIDC(MethodView):

    @blp.response(200)
    def get(self):
        return oidc.user_loggedin
    
@blp.route('/keycloak')
def welcome():
    print(oidc.user_loggedin)
    return {'message': 'login with keycloak successfully!'}

@blp.route('/loginkeycloak' , methods=['GET'])
@oidc.require_login
def loginwithkeycloak():
    print(oidc.user_loggedin)
    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    user_id = info.get('sub')
    username = info.get('preferred_username')
    email = info.get('email')

    # print(info)
    if user_id:
        try:
            access_token = oidc.get_access_token()
            # print ("access_token: %s" % access_token)
            greeting = "access_token: %s" % access_token
        except:
            print ("Could not access greeting-service")
            greeting = "Hello %s" % username
    return {
        'message': 'login with keycloak successfully!',
        'name': username,
        'email': email,
        'id': user_id,
        'access_token': access_token,
        'refresh_token': oidc.get_refresh_token(),
    }

@blp.route('/api', methods=['GET'])
@oidc.accept_token()
def hello_api():
    """OAuth 2.0 protected API endpoint accessible via AccessToken"""

    return {'message': 'Welcome to the API!'}
    
@blp.route('/logoutkeycloak')
def logout():
    """Performs local logout by removing the session cookie."""
    oidc.logout() 
    return 'Hi, you have been logged out! <a href="/">Return</a>'