"""
crupydslparser.grammar._dsl.exception   - DSL exception class
"""
__all__ = [
    'CrupyDslParserException',
]

from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

class CrupyDslParserException(CrupyParserBaseException):
    """ generic DSL exception class
    """
    def __init__(
        self,
        error: CrupyParserBaseException,
        reason: str,
    ) -> None:
        """ generic DSL exception
        """
        super().__init__(
            reason  = reason,
            message = \
                f"DSL parsing exception occured:\n"
                '\n'
                f"{error.context.generate_error_log()}\n"
                '\n'
                f"SyntaxError: {reason}",
        )
