"""
test.crupydataclass - custom implementation of dataclass
"""
__all__ = [
    'CrupyUnittestUtilsDataclass',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser._utils import crupydataclass

#---
# Public
#---

@crupydataclass
class TestClass():
    """ test dataclass """
    test: int
    oui: str

@crupydataclass
class TestClassNested():
    """ test nested init """
    test: int
    oui: str
    def __init__(self) -> None:
        print('NESTED INIT')
        self.nested = 'yes'
        self.test = -1
        self.oui = 'salut a tous'

class CrupyUnittestUtilsDataclass(CrupyUnittestBase):
    """ unittest for custom dataclass
    """
    def test_obj(self) -> None:
        """ test simple init """
        obj = TestClass(test=8, oui='deadbeef')
        self.assertEqual(obj.test, 8)
        self.assertEqual(obj.oui, 'deadbeef')

    def test_nested_init(self) -> None:
        """ test nested init """
        obj = TestClassNested(test=8, oui='deadbeef')
        self.assertEqual(obj.test, -1)
        self.assertEqual(obj.oui, 'salut a tous')
        self.assertEqual(obj.nested, 'yes')
