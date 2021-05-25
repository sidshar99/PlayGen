from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()

class Accounts(db.Model):
    __tablename__ = 'accounts'
    email = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

class Songs(db.Model):
    __tablename__ = 'songs'
    album = db.Column(db.String(250), nullable=False)
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    uri = db.Column(db.String(250), unique = True, nullable=False)

    acousticness = db.Column(db.Float, nullable=False)
    danceability = db.Column(db.Float, nullable=False)
    energy = db.Column(db.Float, nullable=False)
    instrumentalness = db.Column(db.Float, nullable=False)
    liveness = db.Column(db.Float, nullable=False)
    loudness = db.Column(db.Float, nullable=False)
    speechiness = db.Column(db.Float, nullable=False)
    tempo = db.Column(db.Float, nullable=False)
    valence = db.Column(db.Float, nullable=False)
    popularity = db.Column(db.Float, nullable=False)
    
    artist = db.Column(db.String(250), nullable=False)

    def __init__(self, album, id, name, uri, acousticness, danceability, energy, instrumentalness,
                   liveness, loudness, speechiness, tempo, valence, popularity, artist):
        self.album = album
        self.id = id
        self.name = name
        self.uri = uri
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.speechiness = speechiness
        self.tempo = tempo
        self.valence = valence
        self.popularity = popularity
        self.artist = artist


class AccountSchema(ma.Schema):
    email = fields.String(required=True, validate=validate.Length(1))
    password = fields.String(required=True, validate=validate.Length(1))

class SongsSchema(ma.Schema):
    album = fields.String(required=True, validate=validate.Length(1))
    id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    uri = fields.String(required=True, validate=validate.Length(1))
    acousticness = fields.Float(required=True)
    danceability = fields.Float(required=True)
    energy = fields.Float(required=True)
    instrumentalness = fields.Float(required=True)
    liveness = fields.Float(required=True)
    loudness = fields.Float(required=True)
    speechiness = fields.Float(required=True)
    tempo = fields.Float(required=True)
    valence = fields.Float(required=True)
    popularity = fields.Float(required=True)
    artist = fields.String(required=True, validate=validate.Length(1))