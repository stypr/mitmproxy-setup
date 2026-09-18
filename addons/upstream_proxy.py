import asyncio
import random
import struct
import time
import logging

from mitmproxy import http, dns
from mitmproxy.net.server_spec import ServerSpec
from mitmproxy.connection import Server
from mitmproxy.net.dns import response_codes

class UpstreamProxy:
    """
        Empty proxy_servers if you don't plan to use proxy at all
    """
    proxy_servers = [
        ("10.72.72.4", 1080)
    ]

    resolver_servers = [
        ("1.1.1.1", 53)
    ]

    def get_resolver_address(self) -> tuple[str, int]:
        """
        Load balancing based on random.choice
        """
        return random.choice(self.resolver_servers) if self.resolver_servers else None

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


    async def dns_request(self, flow: dns.DNSFlow) -> None:
        proxy_address = self.get_proxy_address()
        resolver_address = self.get_resolver_address()
        if not proxy_address:
            return

        try:
            flow.response = await self.query_dns_via_http_proxy(
                proxy_address,
                resolver_address,
                flow.request,
            )

        except Exception as e:
            logging.exception(
                "DNS proxy failed for %s: %s",
                flow.request.question.name
                if flow.request.question
                else "?",
                e,
            )

            flow.response = flow.request.fail(
                response_codes.SERVFAIL
            )

    async def query_dns_via_http_proxy(
        self,
        proxy: tuple[str, int],
        resolver: tuple[str, int],
        request: dns.DNSMessage,
    ) -> dns.DNSMessage:

        reader, writer = await asyncio.open_connection(
            proxy[0],
            proxy[1],
        )

        try:
            resolver_host, resolver_port = resolver
            target = f"{resolver_host}:{resolver_port}"

            # Request for HTTP proxy
            connect_request = (
                f"CONNECT {target} HTTP/1.1\r\n"
                f"Host: {target}\r\n"
                f"Proxy-Connection: keep-alive\r\n"
                f"\r\n"
            ).encode("ascii")

            writer.write(connect_request)
            await writer.drain()

            headers = await reader.readuntil(b"\r\n\r\n")

            status_line = headers.split(b"\r\n", 1)[0]
            parts = status_line.split(b" ", 2)

            if len(parts) < 2:
                raise RuntimeError(
                    f"Invalid proxy response: {status_line!r}"
                )

            status = int(parts[1])

            if not 200 <= status < 300:
                raise RuntimeError(
                    f"HTTP proxy CONNECT failed: "
                    f"{status_line.decode(errors='replace')}"
                )

            # TCP DNS: uint6 length, DNS packet
            payload = request.packed

            writer.write(
                struct.pack("!H", len(payload))
                + payload
            )
            await writer.drain()

            size_data = await reader.readexactly(2)
            size = struct.unpack("!H", size_data)[0]
            response_data = await reader.readexactly(size)

            return dns.DNSMessage.unpack(
                response_data,
                timestamp=time.time(),
            )

        finally:
            writer.close()

            try:
                await writer.wait_closed()
            except Exception:
                pass
