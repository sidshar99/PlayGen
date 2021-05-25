from flask import Blueprint
from flask_restful import Api
from resources.Songs import SongsResource
from resources.Login import LoginResource
from resources.Logout import LogoutResource
from resources.Register import RegisterResource
from resources.GetPlaylist import PlaylistsResource


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(SongsResource, '/Songs')
api.add_resource(LoginResource, '/Login')
api.add_resource(LogoutResource, '/Logout')
api.add_resource(RegisterResource, '/Register')
api.add_resource(PlaylistsResource, '/Playlist')
