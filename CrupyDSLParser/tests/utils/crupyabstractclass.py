"""
tests.utils.crupyabstractclass  - test custom abstract class
"""
from typing import Any

from crupydslparser._utils import crupyabstractclass
from crupydslparser.exception import CrupyDSLCoreException

#---
# Internals
#---

# Allow too few public methods
# pylint: disable=locally-disabled,R0903

@crupyabstractclass
class _TestA():
    """ test a """

@crupyabstractclass
class _TestAbis():
    """ test a bis """
    def __init__(self, gang: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.gang = gang
        self.only = 'fan'

@crupyabstractclass
class _TestADoubleBis():
    """ test a bis """
    def __init__(self, poungi: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.poungi = poungi

class _TestB(_TestA):
    """ test b """

class _TestC(_TestA):
    """ test c """
    def __init__(self, test: str, ekip: int) -> None:
        self.test = test
        self.ekip = ekip

class _TestD(_TestAbis):
    """ test d """
    def __init__(self, test: str, ekip: int, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.test = test
        self.ekip = ekip

class _TestE(_TestADoubleBis, _TestAbis):
    """ test e """
    def __init__(self, test: str, ekip: int, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.test = test
        self.ekip = ekip

#---
# Public
#---

def test_basic() -> None:
    """ basic test
    """
    assert _TestB() is not None
    try:
        _TestA()
        raise AssertionError('_TestA() instanciated')
    except CrupyDSLCoreException:
        pass

def test_child_init() -> None:
    """ test child init
    """
    obj = _TestC('nrmnra', ekip=667)
    assert obj is not None
    assert obj.test == 'nrmnra'
    assert obj.ekip == 667

def test_parent_init() -> None:
    """ test parent init
    """
    obj = _TestD('fatal', ekip=667, gang='woik')
    assert obj is not None
    assert obj.test == 'fatal'
    assert obj.ekip == 667
    assert obj.gang == 'woik'
    assert obj.only == 'fan'

def test_multiple_parent() -> None:
    """ test multiple parent
    """
    obj = _TestE('kevin', ekip=667, gang='woik', poungi='racaille')
    assert obj is not None
    assert obj.test == 'kevin'
    assert obj.ekip == 667
    assert obj.gang == 'woik'
    assert obj.poungi == 'racaille'
    assert obj.only == 'fan'
