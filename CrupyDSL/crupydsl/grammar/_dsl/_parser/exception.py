"""
crupydsl.grammar._dsl.exception   - DSL exception class
"""
__all__ = [
    'CrupyDSLParserException',
]

from crupydsl.parser.exception import CrupyDSLParserBaseException

#---
# Public
#---

class CrupyDSLParserException(CrupyDSLParserBaseException):
    """ generic DSL exception class
    """
    def __init__(
        self,
        error: CrupyDSLParserBaseException,
        reason: str,
    ) -> None:
        """ generic DSL exception
        """
        super().__init__(
            context = error.context,
            reason  = reason,
            message = \
                'DSL parsing exception occured:\n'
                '\n'
                f"{error.context.generate_error_log()}\n"
                f"SyntaxError: {reason}",
        )
