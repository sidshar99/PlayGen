from flask import request
from flask_marshmallow import schema
from flask_restful import Resource
from Model import db, Songs, SongsSchema

songs_schema = SongsSchema(many=True)
song_schema = SongsSchema()

class SongsResource(Resource):
    def get(self):
        songs = Songs.query.all()
        songs = songs_schema.dump(songs).data
        return {'status': 'success', 'data': songs}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = song_schema.load(json_data)
        if errors:
            return errors, 422
        song = Songs.query.filter_by(id=data['id']).first()
        if song:
            return {'message': 'Song already exists'}, 400
        song = Songs(
            album = json_data['album'],
            id = json_data['id'],
            name = json_data['name'],
            uri = json_data['uri'],
            acousticness = json_data['acousticness'],
            danceability = json_data['danceability'],
            energy = json_data['energy'],
            instrumentalness = json_data['instrumentalness'],
            liveness = json_data['liveness'],
            loudness = json_data['loudness'],
            speechiness = json_data['speechiness'],
            tempo = json_data['tempo'],
            valence = json_data['valence'],
            popularity = json_data['popularity'],
            artist = json_data['artist']
            )

        db.session.add(song)
        db.session.commit()

        result = song_schema.dump(song).data

        return { "status": 'success', 'data': result }, 200
    
    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = song_schema.load(json_data)
        if errors:
            return errors, 400
        song = Songs.query.filter_by(id=data['id']).first()
        if not song:
            return {'message': 'Song does not exist'}, 400
        song.album = json_data['album'],
        song.id = json_data['id'],
        song.name = json_data['name'],
        song.uri = json_data['uri'],
        song.acousticness = json_data['acousticness'],
        song.danceablity = json_data['danceablity'],
        song.energy = json_data['energy'],
        song.instrumentalness = json_data['instrumentalness'],
        song.liveness = json_data['liveness'],
        song.loudness = json_data['loudness'],
        song.speechiness = json_data['speechiness'],
        song.tempo = json_data['tempo'],
        song.valence = json_data['valence'],
        song.popularity = json_data['popularity'],
        song.artist = json_data['artist']

        db.session.commit()

        result = song_schema.dump(song).data

        return { "status": 'success', 'data': result }, 200
    
    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = song_schema.load(json_data)
        if errors:
            return errors, 422
        song = Songs.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = song_schema.dump(song).data

        return { "status": 'success', 'data': result}, 200