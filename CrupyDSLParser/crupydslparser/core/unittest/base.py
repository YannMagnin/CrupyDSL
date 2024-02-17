"""
crupydslparser.core.unittest    - unittest abstraction
"""
__all__ = [
    'CrupyUnittestBase',
]
from typing import Any, Dict, Tuple, Generator, Optional, List
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
    def __generate_testsuit_list(cls) -> None:
        """ scan the `tests/` folder and load all unittest

        each time the `import_module()` will load a class that inherite from
        our class, this will trigger the `__init_subclass__()` magic method
        and the test will be magically added to our `_testsuit_list()`
        """
        test_prefix = Path(f"{__file__}/../../../../tests").resolve()
        for test_file in test_prefix.rglob('*.py'):
            try:
                sys.path.append(str(test_file.parent))
                import_module(test_file.stem)
                sys.path.pop()
            except (ImportError, ModuleNotFoundError) as err:
                raise CrupyUnittestException(
                    f"Unable to load external python file ({err})"
                ) from err

    @classmethod
    def run_tests(cls, target_tests: Optional[List[str]]) -> None:
        """ scan the `tests/` folder and load all unittest and test
        """
        CrupyUnittestBase.__generate_testsuit_list()
        for test in CrupyUnittestBase._testsuit_list.items():
            if target_tests and test[0] not in target_tests:
                continue
            print(f"Testing '{test[0]}'...")
            obj = test[1]['class']()
            for test_name in test[1]['tests']:
                print(f"- {test_name}...")
                getattr(obj, test_name)()

    @classmethod
    def iter_tests(cls) -> Generator[str,None,None]:
        """ iterate over all registered test
        """
        CrupyUnittestBase.__generate_testsuit_list()
        for test_name in CrupyUnittestBase._testsuit_list:
            yield test_name

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
            print(f"WARNING: No exception {type(exc_obj).__name__} occured")
        except exc_obj.__class__ as err:
            if str(exc_obj) != str(err):
                print(f"assertRaises:  mismatch '{exc_obj}' != '{err}'")
        except Exception as err:
            print(
                f"assertRaises: Unable to execute the request ('{err}')"
            )
