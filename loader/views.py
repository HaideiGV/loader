from pyramid.view import view_config


@view_config(route_name='index', renderer='templates/layout.jinja2')
def index(request):
    return {'project': 'loader'}
