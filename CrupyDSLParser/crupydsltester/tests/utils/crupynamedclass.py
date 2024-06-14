"""
test.crupynamedclass - custom class declaration
"""
__all__ = [
    'CrupyUnittestUtilsNamed',
]
from typing import Any

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser._utils import crupynamedclass
from crupydslparser.exception import CrupyDSLCoreException

#---
# Public
#---

@crupynamedclass(
    generate_type   = True,
    regex           = '^Test(?P<type>([A-Z][a-z]+)+)$',
    error           = 'malformated test class',
)
class TestBase():
    """ test a """

class TestTypeName(TestBase):
    """ test b """

class Testouinon(TestBase):
    """ test c """

class TestParent(TestTypeName):
    """ test d"""

class CrupyUnittestUtilsNamed(CrupyUnittestBase):
    """ unittest for custom dataclass
    """
    def test_obj(self) -> None:
        """ test simple init """
        obj = TestTypeName()
        self.assertEqual(obj.type, 'type_name') # type: ignore

    def test_bad_name(self) -> None:
        """ test bad class name """
        try:
            Testouinon()
            self.assertAlways('Testouinon has been instanciated')
        except CrupyDSLCoreException:
            pass

    def test_parent(self) -> None:
        """ test parent """
        obj = TestParent()
        self.assertEqual(obj.type, 'parent')    # type: ignore
