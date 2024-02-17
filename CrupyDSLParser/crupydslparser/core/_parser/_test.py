"""
crupydslparser.core._parser._test   - special parser test class
"""
__all__ = [
    'CrupyParserTest',
]
from typing import Any

from crupydslparser.core._parser._base import CrupyParserBase
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyParserTest(CrupyParserBase):
    """ special test class
    """
    def __init__(
        self,
        production_test: str,
        production_book: Any,
    ) -> None:
        super().__init__(production_book)
        self._stream = CrupyStream.from_any(production_test)
