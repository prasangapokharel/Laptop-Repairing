"""
ORJSON parser for fast JSON parsing
"""
import orjson
from rest_framework.parsers import BaseParser


class ORJSONParser(BaseParser):
    """Fast JSON parser using orjson"""
    media_type = 'application/json'

    def parse(self, stream, media_type=None, parser_context=None):
        data = stream.read()
        return orjson.loads(data)
