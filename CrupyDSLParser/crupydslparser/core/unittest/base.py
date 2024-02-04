"""
crupydslparser.core.unittest    - unittest abstraction
"""
__all__ = [
    'CrupyUnittestBase',
]
from typing import Any, Dict, Tuple
from pathlib import Path
from importlib import import_module
import sys
import re

from crupydslparser.core.unittest.exception import CrupyUnittestException

#---
# Public
#---

class CrupyUnittestBase():
    """ custom unittest uframwork
    """

    #---
    # Register magics
    #---

    _testsuit_list: Dict[str,Any] = {}

    def __init_subclass__(cls, /, **kwargs: Any) -> None:
        """ register all subclass information
        {
            <test_name> : {
                'class' : <class object>,
                'tests' : [
                    <class object special method name>,
                    ...
                ],
            },
            ...
        }
        """
        super().__init_subclass__(**kwargs)
        if not (
            info := re.match(
                "(?P<cls>^CrupyUnittest(?P<key>[a-zA-Z]+)$)",
                cls.__name__,
            )
        ):
            raise CrupyUnittestException(
                f"Subclass name '{cls.__name__}' is not valid, abord",
            )
        print(f"register unittest subclass '{cls.__name__}'")
        if cls.__name__ in CrupyUnittestBase._testsuit_list:
            raise CrupyUnittestException(
                f"Subclass '{cls.__name__}' already exists"
            )
        tests_list = [
            x
            for x in cls.__dict__
                if callable(getattr(cls, x)) and x.startswith('test_')
        ]
        if not tests_list:
            print(f"WARNING: unable to find test method in {cls.__name__}")
            return
        CrupyUnittestBase._testsuit_list[info['key'].lower()] = {
            'class' : cls,
            'tests' : tests_list,
        }

    #---
    # class methods
    #---

    @classmethod
    def run_all_tests(cls) -> None:
        """ scan the `tests/` folder and load all unittest
        """
        test_prefix = Path(f"{__file__}/../../../../tests").resolve()
        for test_file in test_prefix.rglob('*.py'):
            print(test_file)
            try:
                sys.path.append(str(test_file.parent))
                import_module(test_file.stem)
                sys.path.pop()
            except (ImportError, ModuleNotFoundError) as err:
                raise CrupyUnittestException(
                    f"Unable to load external python file ({err})"
                ) from err
        for test in CrupyUnittestBase._testsuit_list.items():
            print(f"Testing '{test[0]}'...")
            obj = test[1]['class']()
            for test_name in test[1]['tests']:
                print(f"- {test_name}...")
                getattr(obj, test_name)()

    #---
    # Public methods
    #---

    # Allow method name in camel case. This to be compliant with the
    # original `unittest` framework used before
    # pylint: disable=locally-disabled,C0103

    def assertEqual(self, first: Any, second: Any) -> None:
        """ simply check if the two objects are equal using '===' """
        try:
            assert first == second
        except AssertionError:
            print(f"assert '{first}' != '{second}'")

    def assertIsNone(self, obj: Any) -> None:
        """ simply check if the object is None """
        assert obj is None

    def assertIsNotNone(self, obj: Any) -> None:
        """ simply check if the object is None """
        assert obj is not None

    # Allow method to catch too general exception
    # pylint: disable=locally-disabled,W0718

    def assertRaises(self, exc_obj: Any, request: Tuple[Any,...]) -> None:
        """ check if the request raise exception """
        try:
            getattr(request[0], request[1])(*request[2:])
        except exc_obj.__class__ as err:
            if str(exc_obj) != str(err):
                print(f"assertRaises:  mismatch '{exc_obj}' != '{err}'")
        except Exception as err:
            print(
                f"assertRaises: Unable to execute the request ('{err}')"
            )
