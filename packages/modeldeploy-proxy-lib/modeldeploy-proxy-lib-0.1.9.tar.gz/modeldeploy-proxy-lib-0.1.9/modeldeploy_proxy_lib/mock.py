import os
from io import BytesIO
import json
from json import dumps, loads
import requests
from werkzeug import wrappers
import urllib

def fill_request_content(request, url, method, **kwargs):
    parsed_result = urllib.parse.urlparse(url)
    request_content = {
        'url': url,
        'method': method
    }
    if parsed_result.scheme:
        request_content['scheme'] = parsed_result.scheme
    if parsed_result.netloc:
        request_content['netloc'] = parsed_result.netloc
    if parsed_result.path:
        request_content['path'] = parsed_result.path
    if parsed_result.params:
        request_content['args'] = parsed_result.params
    if parsed_result.query:
        request_content['query'] = parsed_result.query
    if parsed_result.fragment:
        request_content['fragment'] = parsed_result.fragment
    if parsed_result.hostname:
        request_content['hostname'] = parsed_result.hostname
    if parsed_result.port:
        request_content['port'] = parsed_result.port
    if 'headers' in kwargs and kwargs.get('headers', None):
        request_content['headers'] = kwargs.get('headers')
    if 'form' in kwargs and kwargs.get('form', None):
        request_content['form'] = kwargs.get('form')
    if 'data' in kwargs and kwargs.get('data', None):
        request_content['data'] = kwargs.get('data')
    if 'files' in kwargs and kwargs.get('files', None):
        request_content['files'] = kwargs.get('files')

    for key, value in request_content.items():
        setattr(request, key, value)

    return request

class MockPreprocessInputRetriever():
    @staticmethod
    def get(url, params = None, **kwargs):
        r"""Retrieve the mock input argument of preprocess function.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response

        Usage: the input argument is useful while implementing the pretprocess function.
        """
        request = wrappers.Request.from_values(url)
        request = fill_request_content(request, url, 'GET', params = params)
        return request

    @staticmethod
    def post(url, data = None, json = None, **kwargs):
        r"""Retrieve the input argument of preprocess function as sending a POST request to the url.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Request <werkzeug.wrappers.Request>` object
        :rtype: werkzeug.wrappers.Request

        Usage: the input argument is useful while implementing the preprocess function.
        """

        # read files data first to avoid empty content issue
        files_data = None
        if 'files' in kwargs:
            files = kwargs.get('files')
            files_data = (b"")
            for _file in files:
                if files_data:
                    files_data += (b"\r\n")
                files_data += (b"--boundary\r\n")
                files_data += (b'Content-Disposition: form-data; name="') + _file.encode() + (b'"; filename="') + files.get(_file).name.encode() + (b'"\r\n')
                files_data += (b"\r\n")
                files_data += files.get(_file).read()
                files_data += (b"\r\n")
                files_data += (b"--boundary--")

        if 'files' in kwargs:
            request = wrappers.Request.from_values(
                input_stream = BytesIO(files_data),
                content_length = len(files_data),
                content_type = "multipart/form-data; boundary=boundary",
            )
            headers = {
                'Content-Length': len(files_data),
                'Content-Type': "multipart/form-data; boundary=boundary"
            }
            request = fill_request_content(request, url, 'POST', headers = headers)
        else:
            request = wrappers.Request.from_values(url)
            request = fill_request_content(request, url, 'POST')

        if data:
            request.data = data
        elif json:
            request.data = dumps(json)

        return request

    @staticmethod
    def put(url, data = None, **kwargs):
        r"""Retrieve the input argument of preprocess function as sending a PUT request to the url.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Request <werkzeug.wrappers.Request>` object
        :rtype: werkzeug.wrappers.Request

        Usage: the input argument is useful while implementing the preprocess function.
        """

        # read files data first to avoid empty content issue
        files_data = None
        if 'files' in kwargs:
            files = kwargs.get('files')
            files_data = (b"")
            for _file in files:
                if files_data:
                    files_data += (b"\r\n")
                files_data += (b"--boundary\r\n")
                files_data += (b'Content-Disposition: form-data; name="') + _file.encode() + (b'"; filename="') + files.get(_file).name.encode() + (b'"\r\n')
                files_data += (b"\r\n")
                files_data += files.get(_file).read()
                files_data += (b"\r\n")
                files_data += (b"--boundary--")

        if 'files' in kwargs:
            request = wrappers.Request.from_values(
                input_stream = BytesIO(files_data),
                content_length = len(files_data),
                content_type = "multipart/form-data; boundary=boundary",
            )
            headers = {
                'Content-Length': len(files_data),
                'Content-Type': "multipart/form-data; boundary=boundary"
            }
            request = fill_request_content(request, url, 'PUT', headers = headers)
        else:
            request = wrappers.Request.from_values(url)
            request = fill_request_content(request, url, 'POST')

        if data:
            request.data = data

        return request

class MockPostprocessInputRetriever():
    def __init__(self, mock_data = ""):
        self.mock = mock_data

    def make_response(this):
        response = requests.models.Response()
        response.code = "ok"
        response.status_code = 200
        try:
            if isinstance(this.mock, dict):
                response._content = dumps(this.mock).encode()
                response.headers['Content-Type'] = "application/json"
                return response
            elif isinstance(this.mock, str):
                response._content = dumps(loads(this.mock)).encode()
                response.headers = {'content-type': "application/json"}
                return response
        except (ValueError, TypeError) as e:
            if isinstance(this.mock, str):
                response._content = this.mock.encode()
                response.headers['Content-Type'] = "text/plain"
                return response
            else:
                print(str(e))
                return ValueError("The mock data cannot be serializable.")
        return response

    def get(self, url, params = None, **kwargs):
        r"""Retrieve the input argument of postprocess function as sending a GET request to the url,
        the request will be processed by the preprocess function and the model inference,
        then the result from the model inference will be returned.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response

        Usage: the input argument is useful while implementing the postprocess function.
        """
        return self.make_response()

    def post(self, url, data = None, json = None, **kwargs):
        r"""Retrieve the input argument of postprocess function as sending a POST request to the url,
        the request will be processed by the preprocess function and the model inference,
        then the result from the model inference will be returned.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Request <werkzeug.wrappers.Request>` object
        :rtype: werkzeug.wrappers.Request

        Usage: the input argument is useful while implementing the postprocess function.
        """
        return self.make_response()

    def put(self, url, data = None, **kwargs):
        r"""Retrieve the input argument of postprocess function as sending a PUT request to the url,
        the request will be processed by the preprocess function and the model inference,
        then the result from the model inference will be returned.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Request <werkzeug.wrappers.Request>` object
        :rtype: werkzeug.wrappers.Request

        Usage: the input argument is useful while implementing the preprocess function.
        """
        return self.make_response()
