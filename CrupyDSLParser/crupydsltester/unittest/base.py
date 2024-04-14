"""
crupydsltester.unittest    - unittest abstraction
"""
__all__ = [
    'CrupyUnittestBase',
]
from typing import Any, Optional, NoReturn
from collections.abc import Generator
from pathlib import Path
from importlib import import_module
import traceback
import sys
import re

from crupydsltester.unittest.exception import CrupyUnittestException

#---
# Public
#---

class CrupyUnittestBase():
    """ custom unittest uframwork
    """

    #---
    # Register magics
    #---

    _testsuit_list: dict[str,Any] = {}

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
        name = ''
        for letter in info['key']:
            if name and letter.isupper():
                name += '_'
            name += letter.lower()
        CrupyUnittestBase._testsuit_list[name] = {
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
        test_prefix = Path(f"{__file__}/../../tests").resolve()
        for test_file in test_prefix.rglob('*.py'):
            try:
                sys.path.append(str(test_file.parent))
                import_module(test_file.stem)
                sys.path.pop()
            except (ImportError, ModuleNotFoundError) as err:
                print(
                    '\033[0;31m'
                    f"Unable to load external python file '{test_file}' "
                    f"({err})"
                    '\033[0m'
                )

    @classmethod
    def run_tests(cls, target_tests: Optional[list[str]]) -> None:
        """ scan the `tests/` folder and load all unittest and test
        """
        CrupyUnittestBase.__generate_testsuit_list()
        for test in CrupyUnittestBase._testsuit_list.items():
            if target_tests and test[0] not in target_tests:
                continue
            print(f"\033[1;97mTesting '{test[0]}'...\033[0m")
            obj = test[1]['class']()
            for test_name in test[1]['tests']:
                print(f"- {test_name}...")
                try:
                    getattr(obj, test_name)()
                # allow general exception handling
                # pylint: disable=locally-disabled,W0718
                except Exception as err:
                    cls._error(
                        '!!! Exception during test execution -> '
                        f"{traceback.format_exc()} "
                        f"({err.__class__.__name__}) "
                        f"{err}"
                    )

    @classmethod
    def iter_tests(cls) -> Generator[str,None,None]:
        """ iterate over all registered test
        """
        CrupyUnittestBase.__generate_testsuit_list()
        yield from CrupyUnittestBase._testsuit_list

    #---
    # Internals
    #---

    @classmethod
    def _error(cls, text: str) -> None:
        """ display text in bold red """
        print(f"\033[1;31m{text}\033[0m", file=sys.stderr)

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
            self._error(f"assert '{first}' != '{second}'")

    def assertIsNone(self, obj: Any) -> None:
        """ simply check if the object is None """
        try:
            assert obj is None
        except AssertionError:
            self._error(f"assert '{obj}' is not None")

    def assertIsNotNone(self, obj: Any) -> None:
        """ simply check if the object is None """
        try:
            assert obj is not None
        except AssertionError:
            self._error(f"assert '{obj}' is None")

    # Allow method to catch too general exception
    # pylint: disable=locally-disabled,W0718

    def assertRaises(
        self,
        cls_exc: Any,
        request: tuple[Any,...],
        error: str,
    ) -> None:
        """ check if the request raise exception """
        try:
            getattr(request[0], request[1])(*request[2:])
            self._error(
                f"WARNING: No exception {type(cls_exc).__name__} occured"
            )
        except cls_exc as err:
            if error != str(err):
                self._error(
                    f"assertRaises:  mismatch '{error}' != '{err}'"
                )
        except Exception as err:
            self._error(
                f"assertRaises: Unable to execute the request ('{err}')"
            )

    def assertAlways(self, text: str) -> NoReturn:
        """ always raise exception """
        raise CrupyUnittestException(text)
