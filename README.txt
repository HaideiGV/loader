loader README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/pip install -e .

- $VENV/bin/pserve development.ini








API EXAMPLES
=================

GET:

- curl -i -X GET http://localhost:6565/get/<file_key>


POST:


    Request:

        - curl -i -X POST -H "Content-Type: multipart/form-data" -F "data=<file_path>" http://localhost:6565/post

    Response:

        HTTP/1.1 100 Continue

        HTTP/1.1 200 OK
        Content-Length: 54
        Content-Type: application/json
        Date: Sat, 24 Jun 2017 20:44:56 GMT
        Server: waitress

        {
            "file_key": "a2149e38bdf947d4ada09ab1f98706c6"
        }%