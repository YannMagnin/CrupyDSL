"""
tests.stream.stream     - stream object unittest
"""
__all__ = [
    'CrupyUnittestStream',
]
from typing import Tuple

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyUnittestStream(CrupyUnittestBase):
    """ unittest suit for the crypu stream object
    """

    #---
    # Internal tests
    #---

    def _split_test(self, lexem_list: Tuple[str,...], text: str) -> None:
        """ common code for lexem splitting testing
        """
        stream = CrupyStream.from_string(text)
        for lexem_target in lexem_list:
            with stream as lexem:
                self.assertEqual(lexem.read(), lexem_target)
                lexem.validate()

    #---
    # Public tests
    #---

    def test_read_peek(self) -> None:
        """ simply check the read/peek
        """
        stream = CrupyStream.from_any('abcd')
        for ctest in 'abcd':
            self.assertEqual(stream.peek_char(), ctest)
            self.assertEqual(stream.read_char(), ctest)
        self.assertIsNone(stream.peek_char())
        self.assertIsNone(stream.read_char())

    def test_lexem(self) -> None:
        """ simply check the `with` context for only one lexem
        """
        with CrupyStream.from_any('abcd') as lexem:
            self.assertEqual(lexem.read(), 'abcd')
            self.assertIsNone(lexem.read())
        with CrupyStream.from_any('     abcd    ') as lexem:
            self.assertEqual(lexem.read(), 'abcd')
            self.assertIsNone(lexem.read())

    def test_lexem_split_space(self) -> None:
        """ check whole lexem splitting only with sigle space char
        """
        self._split_test(
            ('01234', '9876<>', '0xdeadbeef'),
            '01234 9876<> 0xdeadbeef',
        )

    def test_lexem_split_any(self) -> None:
        """ check lexem splitting with all possible separator
        """
        lexem_list = (
            'dsgfsfddfs',
            '38f857e2667',
            r'<>/?\\"ldkfms[jsfnpjfnwfv',
        )
        self._split_test(
            lexem_list,
            f"""
            {lexem_list[0]}\t\t\v\r{lexem_list[1]}

                 \t{lexem_list[2]}
           """,
       )

    def test_end_of_file(self) -> None:
        """ check the end of file exception
        """
        stream = CrupyStream.from_any('abcd      func_name(oui)  ')
        with stream as lexem:
            self.assertEqual(lexem.read_char(), 'a')
            self.assertEqual(lexem.read_char(), 'b')
            lexem.validate()
        with stream as lexem:
            self.assertEqual(lexem.read_char(), 'c')
            self.assertEqual(lexem.read_char(), 'd')
            self.assertIsNone(lexem.read_char())
            self.assertIsNone(lexem.read_char())
        with stream as lexem:
            self.assertEqual(lexem.read(), 'cd')
            self.assertIsNone(lexem.read_char())
            lexem.validate()
        with stream as lexem:
            self.assertEqual(lexem.read(), 'func_name(oui)')
            lexem.validate()
        with stream as lexem:
            self.assertIsNone(lexem.read())
            lexem.validate()
        with stream as lexem:
            self.assertIsNone(lexem.read())
            lexem.validate()

    def test_context(self) -> None:
        """ check context handling
        """
        stream = CrupyStream.from_any('abcdef')
        with stream as lexem:
            self.assertEqual(lexem.read_char(), 'a')
            self.assertEqual(lexem.read_char(), 'b')
            with stream as lexem2:
                self.assertEqual(lexem2.read_char(), 'c')
                lexem2.validate()
            self.assertEqual(lexem.read_char(), 'd')
        with stream as lexem:
            self.assertEqual(lexem.read_char(), 'a')
            self.assertEqual(lexem.read_char(), 'b')
            with stream as lexem2:
                self.assertEqual(lexem2.read_char(), 'c')
                with stream as lexem3:
                    self.assertEqual(lexem3.read_char(), 'd')
                    lexem3.validate()
                self.assertEqual(lexem2.read_char(), 'e')
            self.assertEqual(lexem.read_char(), 'c')
