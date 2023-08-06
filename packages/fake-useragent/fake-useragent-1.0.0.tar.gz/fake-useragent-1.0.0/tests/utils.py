import os
import socket
from urllib.request import Request

_used_ports = set()


def find_unused_port():
    while True:
        service = socket.socket()

        try:
            service.bind(("127.0.0.1", 0))

            _, port = service.getsockname()

            if port not in _used_ports:
                break
        finally:
            service.close()

    return port


def _request(*args, **kwargs):
    assert args

    denied_urls = kwargs.pop("denied_urls", [])
    response_url = kwargs.pop("response_url", None)

    requested_url = args[0]

    for url in denied_urls:
        if requested_url.startswith(url):
            if response_url is None:
                response_url = "http://0.0.0.0:{port}".format(
                    port=find_unused_port(),
                )

    if response_url is not None:
        args = list(args)
        args[0] = response_url
        args = tuple(args)
    return Request(*args, **kwargs)
