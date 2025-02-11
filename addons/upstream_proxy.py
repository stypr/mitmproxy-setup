import random
from mitmproxy import http
from mitmproxy.net.server_spec import ServerSpec
from mitmproxy.connection import Server

class UpstreamProxy:
    """
        Empty proxy_servers if you don't plan to use proxy at all
    """
    proxy_servers = [
        ("127.0.0.1", 40000)
    ]

    def get_proxy_address(self) -> tuple[str, int]:
        """
        Load balancing based on random.choice
        """
        return random.choice(self.proxy_servers) if self.proxy_servers else None


    def request(self, flow: http.HTTPFlow) -> None:
        """
        Main Request Handler
        """

        # Forward to Upstream Proxy
        proxy_address = self.get_proxy_address()
        if proxy_address:
            server_connection_already_open = flow.server_conn.timestamp_start is not None
            if server_connection_already_open and proxy_address:
                flow.server_conn = Server(address=flow.server_conn.address)
            flow.server_conn.via = ServerSpec(("http", proxy_address))

