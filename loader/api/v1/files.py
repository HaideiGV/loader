import uuid
import datetime
from gridfs import GridFSBucket
from gridfs.errors import NoFile

from cornice.resource import resource
from pyramid.response import Response


@resource(collection_path='/api/v1/files', path='/api/v1/files/{uuid}')
class File(object):

    def __init__(self, request):
        self.request = request

    def get(self):
        images = self.request.db['images'].find({"client_key": self.request.matchdict['uuid']})

        fs = GridFSBucket(self.request.db)

        file_key = None
        for image in images:
            file_key = image['file_key']

        try:
            data = fs.open_download_stream(file_key)
        except NoFile:
            return Response("FILE NOT FOUND!")

        return Response(data.read())

    def collection_post(self):
        fs = GridFSBucket(self.request.db)

        client_key = uuid.uuid4().hex

        file_data = self.request.body

        if not file_data:
            return Response("FILE DATA MUST BE SPECIFIED!")

        file_id = fs.upload_from_stream(str(client_key), file_data)

        self.request.db['images'].insert(
            {
                'client_key': client_key,
                'file_key': file_id,
                'description': self.request.POST.get('description'),
                'date': datetime.datetime.now()
            }
        )

        return {'file_key': client_key}

    def delete(self):
        images = self.request.db['images'].find({"client_key": self.request.matchdict['uuid']})

        fs = GridFSBucket(self.request.db)

        file_key = None
        for image in images:
            file_key = image['file_key']

        if not file_key:
            return Response("FILE NOT FOUND!")

        fs.delete(file_key)

        return Response("DELETED!")

    def put(self):
        client_uuid = self.request.matchdict['uuid']
        images = self.request.db['images'].find({"client_key": client_uuid})

        fs = GridFSBucket(self.request.db)

        file_key = None
        for image in images:
            file_key = image['file_key']

        file_data = self.request.body

        if not file_data:
            return Response("FILE DATA MUST BE SPECIFIED!")

        fs.delete(file_key)

        file_id = fs.upload_from_stream(str(file_key), file_data)

        self.request.db['images'].insert(
            {
                'client_key': client_uuid,
                'file_key': file_id,
                'description': self.request.POST.get('description')
            }
        )

        return Response("UPDATED!")
