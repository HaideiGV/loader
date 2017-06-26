from urllib.parse import urlparse

from cornice import resource
from pymongo import MongoClient
from pyramid.config import Configurator
from pyramid.renderers import JSON

from loader.api.v1.files import File


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_renderer('img_json', JSON(indent=4))
    config.add_static_view('static', 'static', cache_max_age=3600)

    db_url = urlparse("mongodb://test:test@localhost:27017/loaddb")

    config.registry.db = MongoClient(
        host=db_url.hostname,
        port=db_url.port,
    )

    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db

    config.add_route('index', '/')
    config.add_request_method(add_db, 'db', reify=True)

    user_resource = resource.add_resource(
        File, collection_path='/api/v1/files', path='/api/v1/files/{uuid}'
    )

    config.include("cornice")
    config.add_cornice_resource(user_resource)
    config.scan('loader')
    return config.make_wsgi_app()
