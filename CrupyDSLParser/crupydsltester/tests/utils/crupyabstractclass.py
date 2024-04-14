"""
tests.utils.crupyabstractclass  - test custom abstract class
"""
__all__ = [
    'CrupyUnittestUtilsAbc',
]
from typing import Any

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser._utils import crupyabstractclass
from crupydslparser.exception import CrupyDSLCoreException

#---
# Public
#---

# Allow too few public methods
# pylint: disable=locally-disabled,R0903

@crupyabstractclass
class TestA():
    """ test a """

@crupyabstractclass
class TestAbis():
    """ test a bis """
    def __init__(self, gang: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.gang = gang
        self.only = 'fan'

@crupyabstractclass
class TestADoubleBis():
    """ test a bis """
    def __init__(self, poungi: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.poungi = poungi

class TestB(TestA):
    """ test b """

class TestC(TestA):
    """ test c """
    def __init__(self, test: str, ekip: int) -> None:
        self.test = test
        self.ekip = ekip

class TestD(TestAbis):
    """ test d """
    def __init__(self, test: str, ekip: int, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.test = test
        self.ekip = ekip

class TestE(TestADoubleBis, TestAbis):
    """ test e """
    def __init__(self, test: str, ekip: int, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.test = test
        self.ekip = ekip


class CrupyUnittestUtilsAbc(CrupyUnittestBase):
    """ unittest abstract class
    """
    def test_basic(self) -> None:
        """ basic test """
        self.assertIsNotNone(TestB())
        try:
            TestA()
            self.assertAlways('TestA() instanciated')
        except CrupyDSLCoreException:
            pass

    def test_child_init(self) -> None:
        """ test child init """
        obj = TestC('nrmnra', ekip=667)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.test, 'nrmnra')
        self.assertEqual(obj.ekip, 667)

    def test_parent_init(self) -> None:
        """ test parent init """
        obj = TestD('fatal', ekip=667, gang='woik')
        self.assertIsNotNone(obj)
        self.assertEqual(obj.test, 'fatal')
        self.assertEqual(obj.ekip, 667)
        self.assertEqual(obj.gang, 'woik')
        self.assertEqual(obj.only, 'fan')

    def test_multiple_parent(self) -> None:
        """ test multiple parent """
        obj = TestE('kevin', ekip=667, gang='woik', poungi='racaille')
        self.assertIsNotNone(obj)
        self.assertEqual(obj.test, 'kevin')
        self.assertEqual(obj.ekip, 667)
        self.assertEqual(obj.gang, 'woik')
        self.assertEqual(obj.poungi, 'racaille')
        self.assertEqual(obj.only, 'fan')
