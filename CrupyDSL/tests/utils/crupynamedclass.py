"""
test.crupynamedclass - custom class declaration
"""
from crupydsl._utils import crupynamedclass
from crupydsl.exception import CrupyDSLCoreException

#---
# Internals
#---

# Allow too few public methods
# pylint: disable=locally-disabled,R0903

@crupynamedclass(
    generate_type   = True,
    regex           = '^_Test(?P<type>([A-Z][a-z]+)+)$',
    error           = 'malformated test class',
)
class _TestBase():
    """ test a """

class _TestTypeName(_TestBase):
    """ test b """

class _Testouinon(_TestBase):
    """ test c """

class _TestParent(_TestTypeName):
    """ test d"""

#---
# Public
#---

def test_obj() -> None:
    """ test simple init
    """
    obj = _TestTypeName()
    assert getattr(obj, 'type') == 'type_name'

def test_bad_name() -> None:
    """ test bad class name
    """
    try:
        _Testouinon()
        raise AssertionError('_Testouinon has been instanciated')
    except CrupyDSLCoreException:
        pass

def test_parent() -> None:
    """ test parent
    """
    obj = _TestParent()
    assert getattr(obj, 'type') == 'parent'
