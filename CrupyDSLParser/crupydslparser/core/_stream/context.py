"""
crupydslparser.core._stream.context     - stream context information
"""
__all__ = [
    'CrupyStreamContext',
]
from dataclasses import dataclass

#---
# Public
#---

@dataclass
class CrupyStreamContext():
    """ stream context """
    index:      int
    lineno:     int
    column:     int
