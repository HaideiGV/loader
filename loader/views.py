from pyramid.view import view_config
from pyramid.response import Response
import gridfs
from gridfs import GridFSBucket
from gridfs.errors import NoFile
import uuid


@view_config(route_name='get')
def get(request):

    images = request.db['images'].find({"client_key": request.matchdict['uuid']})

    fs = GridFSBucket(request.db)

    file_key = None
    for image in images:
        file_key = image['file_key']

    try:
        data = fs.open_download_stream(file_key)
    except NoFile:
        return Response("FILE NOT FOUND!")

    return Response(data.read())


@view_config(route_name='index', renderer='templates/layout.jinja2')
def index(request):
    return {'project': 'loader'}


@view_config(route_name='post', renderer='img_json')
def post(request):

    fs = GridFSBucket(request.db)

    client_key = uuid.uuid4().hex

    file_data = request.body

    if not file_data:
        return Response("FILE DATA MUST BE SPECIFIED!")

    file_id = fs.upload_from_stream(str(client_key), file_data)

    request.db['images'].insert(
        {
            'client_key': client_key,
            'file_key': file_id,
            'description': request.POST.get('description')
        }
    )

    return {'file_key': client_key}


@view_config(route_name='delete', renderer='img_json')
def delete(request):

    images = request.db['images'].find({"client_key": request.matchdict['uuid']})

    fs = GridFSBucket(request.db)

    file_key = None
    for image in images:
        file_key = image['file_key']

    if not file_key:
        return Response("FILE NOT FOUND!")

    fs.delete(file_key)

    return Response("DELETED!")


@view_config(route_name='update', renderer='img_json')
def update(request):

    images = request.db['images'].find({"client_key": request.matchdict['uuid']})

    fs = GridFSBucket(request.db)

    file_key = None
    for image in images:
        file_key = image['file_key']

    if not file_key:
        return Response("FILE NOT FOUND!")

    fs.delete(file_key)

    return Response("DELETED!")