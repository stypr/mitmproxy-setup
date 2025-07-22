#!/usr/bin/python3 -u

"""
Main script for debugging

Adds AES auto-decrypt view in the mitmweb
"""

from typing import Optional
import json
import msgpack
from Crypto.Cipher import AES
from mitmproxy.contentviews import Contentview

class SekaiCore:
    # To use this class, you need a valid key and IV.
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


class ViewProjectSekai(Contentview):
    name = "pjsekai"

    def render_priority(
        self,
        data: bytes,
        metadata
    ) -> float:
        """ prioritize using this when priority is set """
        try:
            if not data or not metadata:
                return 0

            decrypt_result = SekaiCore.decrypt_data(data)
            return 1 if decrypt_result else 0
        except Exception as e:
            return 0

    def prettify(
        self,
        data: bytes,
        _
    ) -> str:
        try:
            plaintext: Optional[dict] = SekaiCore.decrypt_data(data)
            return json.dumps(plaintext, indent=4, ensure_ascii=False)
        except Exception as e:
            return e
