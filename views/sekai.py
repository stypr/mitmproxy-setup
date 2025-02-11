#!/usr/bin/python3 -u

"""
Main script for debugging

Adds AES auto-decrypt view in the mitmweb
"""

from typing import Optional
from urllib.parse import urlparse
import msgpack
from Crypto.Cipher import AES
from mitmproxy import contentviews
from mitmproxy import flow
from mitmproxy import http
# from mitmproxy import ctx

class SekaiCore:
    # To use this you need a valid key and IV.
    aes_key = b""
    aes_iv = b""

    @classmethod
    def encrypt_data(cls, plaintext):
        aes_mode = AES.MODE_CBC
        aes_key = cls.aes_key
        aes_iv = cls.aes_iv
        aes = AES.new(aes_key, aes_mode, aes_iv)
        aes_padding = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16).encode()
        plaintext = msgpack.packb(plaintext)
        plaintext = aes_padding(plaintext)
        return aes.encrypt(plaintext)

    @classmethod
    def decrypt_data(cls, crypttext):
        aes_mode = AES.MODE_CBC
        aes_key = cls.aes_key
        aes_iv = cls.aes_iv
        aes = AES.new(aes_key, aes_mode, aes_iv)

        plaintext = aes.decrypt(crypttext)
        try:
            return msgpack.unpackb(plaintext[:-plaintext[-1]], strict_map_key=False)
        except (ValueError, IndexError):
            try:
                return msgpack.unpackb(plaintext, strict_map_key=False)
            except ValueError:
                return {}


class ViewSekai(contentviews.View):
    name = "sekai"

    def __call__(
        self,
        data: bytes,
        *,
        content_type: Optional[str] = None,
        flow: Optional[flow.Flow] = None,
        http_message: Optional[http.Message] = None,
        **unknown_metadata,
    ) -> contentviews.TViewResult:
        """ Decrypts data upon response. """
        try:
            plaintext: Optional[dict] = SekaiCore.decrypt_data(data)
            return "sekai", contentviews.json.format_json(plaintext)
        except Exception as e:
            return "sekai", contentviews.format_text(e)

    def render_priority(
        self,
        data: bytes,
        *,
        content_type: Optional[str] = None,
        flow: Optional[flow.Flow] = None,
        http_message: Optional[http.Message] = None,
        **unknown_metadata,
    ) -> float:
        """ prioritize using this when priority is set """
        try:
            if not data:
                return 0
            _ = SekaiCore.decrypt_data(data)
            return 1
        except Exception as e:
            return 0
