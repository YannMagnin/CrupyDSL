"""
test.crupydataclass - custom implementation of dataclass
"""
from typing import Any

from crupydsl._utils import crupydataclass

#---
# Internals
#---

# Allow too few public methods
# pylint: disable=locally-disabled,R0903

@crupydataclass
class _TestClass():
    """ test dataclass """
    test: int
    oui: str
    def __init__(self, /, **_: Any) -> None:
        """ workaround """

@crupydataclass
class _TestClassNested():
    """ test nested init """
    test: int
    oui: str
    def __init__(self, /, **_: Any) -> None:
        print('NESTED INIT')
        self.nested = 'yes'
        self.test = -1
        self.oui = 'salut a tous'

#---
# Public
#---

def test_obj() -> None:
    """ test simple init
    """
    obj = _TestClass(test=8, oui='deadbeef')
    assert obj.test == 8
    assert obj.oui == 'deadbeef'

def test_nested_init() -> None:
    """ test nested init
    """
    obj = _TestClassNested(test=8, oui='deadbeef')
    assert obj.test == -1
    assert obj.oui == 'salut a tous'
    assert obj.nested == 'yes'
