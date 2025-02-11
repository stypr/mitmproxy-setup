import os
import logging
import tempfile
import requests
from mitmproxy import http

class WebConsole:
    """
    Adds web console for convenient mobile devtools
    You may use vConsole as an alternative.
    """
    console = ""
    console_url = "https://cdn.jsdelivr.net/npm/eruda"

    def load(self, loader):
        console_path = os.path.join(tempfile.gettempdir(), "console.js")

        try:
            self.console = open(console_path).read()
        except:
            logging.warning("Dowloading Eruda to temporary directory...")
            self.console = requests.get(self.console_url, timeout=10).text
            open(console_path, "w").write(self.console)

    def request(self, flow: http.HTTPFlow) -> None:
        """
        Main Request Handler
        """
        match flow.request.path:
            case "/__script__/__console__.js":
                flow.response = http.Response.make(
                    200,
                    self.console,
                    {"Content-Type": "text/javascript"}
                )
            case _:
                pass

    def response(self, flow: http.HTTPFlow) -> None:
        """
        Append console script for all text/html responses
        """

        # Inject Eruda if the response is HTML
        is_html = False
        for key, value in flow.response.headers.items():
            # text/html; charset=utf-8
            if key.lower() == "content-type" and value.startswith("text/html"):
                is_html = True
                break

        if is_html:
            console_loader = b"""
                <script async>
                    (() => {
                        var script3336974aaa = document.createElement('script');
                        script3336974aaa.src="/__script__/__console__.js";
                        document.head.append(script3336974aaa);
                        script3336974aaa.onload = () => { eruda.init(); };
                    })();
                </script></head>
            """
            flow.response.content = flow.response.content.replace(b"</head>", console_loader)
