import os
import logging
import tempfile
import requests
from mitmproxy import http

class Debug:
    """
    Main debug script
    """

    def request(self, flow: http.HTTPFlow) -> None:
        """
        Main Request Handler
        """

        match flow.request.path:
            case "/__ok__":
                flow.response = http.Response.make(200, "ok", {"Content-Type": "text/html"})
            case _:
                pass

    def response(self, flow: http.HTTPFlow) -> None:
        """
        Main Response Handler
        """

        match flow.request.path:
            case "/iam/api/login":
                flow.response.content = flow.response.content.replace(b"true", b"false")
            case _:
                pass
