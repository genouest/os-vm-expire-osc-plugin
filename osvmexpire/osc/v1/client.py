from osvmexpire.common import http

class Client(object):
    """Client for the osvmexpire v1 API.

    :param string endpoint: A user-supplied endpoint URL for the osvmexpire
                            service.
    :param string token: Token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new client for the osvmexpire v1 API."""
        print("##OSALLOU CREATE CLIENT####")
        self.http_client = http._construct_http_client(*args, **kwargs)
