from typing import Any

from parsy import ParseError, Parser

__all__ = ["parser_parses"]


def parser_parses(parser: Parser, value: Any) -> bool:
    try:
        parser.parse_partial(value)
    except ParseError:
        return False
    return True
