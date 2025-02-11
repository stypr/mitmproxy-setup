import os
import logging
import tempfile
import requests
from mitmproxy import http

class NoCache:
    """
    Disable caching completely.
    """

    def response(self, flow: http.HTTPFlow) -> None:
        """
        Disable caching completely.
        """

        # Never ever cache responses.
        flow.response.headers["cache-control"] = "no-cache, no-store, must-revalidate"
        flow.response.headers["pragma"] = "no-cache"
        flow.response.headers["expires"] = "0"
