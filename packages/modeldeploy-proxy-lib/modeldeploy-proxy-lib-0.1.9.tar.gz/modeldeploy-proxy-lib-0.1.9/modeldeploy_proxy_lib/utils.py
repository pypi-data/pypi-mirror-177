from json import dumps, loads
import requests
from werkzeug import wrappers
import urllib
from io import BytesIO

def convert_to_get_preprocess_input_url(url):
    if "?" in url:
        partitions = url.split("?")
        target_url = "{}/get-preprocess-input?{}".format(partitions[0], partitions[1])
    else:
        target_url = "{}/get-preprocess-input".format(url)

    return target_url

def convert_to_get_postprocess_input_url(url):
    if "?" in url:
        partitions = url.split("?")
        target_url = "{}/get-postprocess-input?{}".format(partitions[0], partitions[1])
    else:
        target_url = "{}/get-postprocess-input".format(url)

    return target_url

class PreprocessInputRetriever():
    @staticmethod
    def get(url, params = None, **kwargs):
        r"""Retrieve the input argument of preprocess function as sending a GET request to the url.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response

        Usage: the input argument is useful while implementing the postprocess function.
        """
        target_url = convert_to_get_preprocess_input_url(url)

        response = requests.get(target_url, params = params, **kwargs)
        response = response.json()
        environ_base = response.pop('environ_base', None)
        if environ_base:
            request = wrappers.Request.from_values(environ_base = environ_base)
        else:
            parsed_result = urllib.parse.urlparse(url)
            localhost_url = url.replace(parsed_result.netloc, 'localhost')
            request = wrappers.Request.from_values(localhost_url)

        for key, value in response.items():
            setattr(request, key, value)

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

        target_url = convert_to_get_preprocess_input_url(url)

        response = requests.post(target_url, data = data, json = json, **kwargs)
        response = response.json()
        environ_base = response.pop('environ_base', None)
        if 'files' in kwargs:
            request = wrappers.Request.from_values(
                input_stream = BytesIO(files_data),
                content_length = len(files_data),
                content_type = "multipart/form-data; boundary=boundary",
            )
            response.pop('form', None)
            headers = loads(response.get("headers"))
            headers['Content-Length'] = len(files_data)
            headers['Content-Type'] = "multipart/form-data; boundary=boundary"
            response['headers'] = headers
            for key, value in response.items():
                setattr(request, key, value)
        elif environ_base:
            request = wrappers.Request.from_values(environ_base = environ_base)
            for key, value in response.items():
                setattr(request, key, value)
        else:
            parsed_result = urllib.parse.urlparse(url)
            localhost_url = url.replace(parsed_result.netloc, 'localhost')
            request = wrappers.Request.from_values(localhost_url)
            for key, value in response.items():
                setattr(request, key, value)

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

        target_url = convert_to_get_preprocess_input_url(url)

        response = requests.put(target_url, data = data, **kwargs)
        response = response.json()
        environ_base = response.pop('environ_base', None)
        if environ_base:
            request = wrappers.Request.from_values(environ_base = environ_base)
        else:
            parsed_result = urllib.parse.urlparse(url)
            localhost_url = url.replace(parsed_result.netloc, 'localhost')
            request = wrappers.Request.from_values(localhost_url)

        for key, value in response.items():
            setattr(request, key, value)

        if data:
            request.data = data

        if 'files' in kwargs:
            files = kwargs.get('files')
            request.files = files

        return request

class PostprocessInputRetriever():
    @staticmethod
    def get(url, params = None, **kwargs):
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
        target_url = convert_to_get_postprocess_input_url(url)
        response = requests.get(target_url, params = params, **kwargs)
        return response

    @staticmethod
    def post(url, data = None, json = None, **kwargs):
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

        target_url = convert_to_get_postprocess_input_url(url)
        response = requests.post(target_url, data = data, json = json, **kwargs)
        return response

    @staticmethod
    def put(url, data = None, **kwargs):
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

        target_url = convert_to_get_postprocess_input_url(url)
        response = requests.put(target_url, data = data, **kwargs)
        return response
