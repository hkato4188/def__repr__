#!/usr/bin/env python3

# Standard and remote library imports
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_migrate import Migrate
from flask import Flask, request

# Local imports
from models import db, Post, Tag, User, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Instantiate REST API
api = Api(app)
# Instantiate CORS
CORS(app)

migrate = Migrate(app, db)

db.init_app(app)



# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

