from flask import Flask
from flask_restful import Api
from flask_apispec.extension import FlaskApiSpec

from config import Config
from extensions import db
from resources.book import BookListResource, BookResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    docs = FlaskApiSpec(app)
    docs.register(BookListResource)
    docs.register(BookResource)
    return app


def register_extensions(app):
    db.init_app(app)


def register_resources(app):
    api = Api(app)

    api.add_resource(BookListResource, '/books')
    api.add_resource(BookResource, '/books/<int:book_id>')


if __name__ == '__main__':
    app = create_app()
    app.run()
