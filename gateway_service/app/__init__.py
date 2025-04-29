from flask import Flask
from flask_restx import Api

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Add "Bearer <JWT token>"'
    }
}

def create_app():
    app = Flask(__name__)
    api = Api(app, doc="/swagger", authorizations=authorizations, security="Bearer Auth")
    
    from .user_routes import user_api
    api.add_namespace(user_api, path="/users")

    from .media_routes import media_api
    api.add_namespace(media_api, "/media-management")
    
    return app, api