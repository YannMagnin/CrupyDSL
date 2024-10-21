"""
crupydsl.parser._stream.context   - stream context information
"""
# @note
# Used as a workaround for the cyclic-import and to allow using the
# class name as return type before the said class is finished to be
# declared
from __future__ import annotations

__all__ = [
    'CrupyDSLStreamContext',
]
from typing import TYPE_CHECKING

# @note : Design mistake
#
# We cannot import the `CrupyDSLStream` class since we use the
# `CrupyDSLStreamContext` class in the `CrupyDSLStream`. So, we are in a
# circular dependencies problem.
if TYPE_CHECKING:
    from crupydsl.parser._stream.stream import CrupyDSLStream

#---
# Public
#---

class CrupyDSLStreamContext():
    """ stream context
    """
    def __init__(
        self,
        stream: CrupyDSLStream,
        index: int,
        lineno: int,
        column: int,
    ) -> None:
        self._stream = stream
        self.index  = index
        self.lineno = lineno
        self.column = column
        self.index_start = index

    def __gt__(self, context: CrupyDSLStreamContext) -> bool:
        return self.index > context.index

    def __ge__(self, context: CrupyDSLStreamContext) -> bool:
        return self.index >= context.index

    def __str__(self) -> str:
        info  = f"<{type(self).__name__}: "
        info += f"index={self.index}, "
        info += f"lineno={self.lineno}, "
        info += f"column={self.column}, "
        info += f"index_start={self.index_start}>"
        return info

    #---
    # Public properties
    #---

    @property
    def has_read(self) -> int:
        """ calculated the readded counter """
        return self.index - self.index_start

    #---
    # Public methods
    #---

    ## memory primitives

    def peek_char(self) -> str|None:
        """ return the current char

        @note
        - a special handling is performed for the windows CRLF which is
            concidered as a whole character here to simplify a lot of work in
            line handling
        - the current index will not be modified
        """
        if not (curr := self._stream[self.index]):
            return None
        if (char := chr(curr & 0xff)) != '\r':
            return char
        if curr := self._stream[self.index + 1]:
            if chr(curr & 0xff) == '\n':
                return '\r\n'
        return '\r'


    def read_char(self) -> str|None:
        """ read the current char and update the cursor

        @notes
        - support LF or CRLF as a end of line
        """
        if not (curr := self.peek_char()):
            return None
        if curr == '\n':
            self.index  += 1
            self.lineno += 1
            self.column  = 1
        elif curr == '\r\n':
            self.index  += 2
            self.lineno += 1
            self.column  = 1
        else:
            self.index  += 1
            self.column += 1
        return curr

    ## error handling

    def generate_error_log(self) -> str:
        """ generate error context information

        @note
        - we need to be careful with line spliting with '\n', '\r\n'
        - we need to expand tabs for the displayed line
        """
        line_start_idx = self.index - (self.column - 1)
        rawline = ''
        i = line_start_idx
        while True:
            if not (curr := self._stream[i]):
                break
            if (curr_char := chr(curr & 0xff)) == '\n':
                rawline += '\n'
                break
            if curr_char == '\r':
                if curr := self._stream[i + 1]:
                    if chr(curr & 0xff) == '\n':
                        rawline += '\r\n'
                        break
            rawline += curr_char
            i += 1
        line = rawline
        line = line.expandtabs(tabsize=4)
        line = line.replace('\r', r'\r')
        line = line.replace('\n', r'\n')
        ctx_start_idx = self.index_start - line_start_idx
        ctx_end_idx = self.index - line_start_idx
        error  = f"Stream: line {self.lineno}, column {self.column}\n"
        error += f"{line.expandtabs()}\n"
        if ctx_start_idx > 0:
            magic_padding = rawline[0:ctx_start_idx]
            magic_padding = magic_padding.expandtabs(tabsize=4)
            magic_padding = magic_padding.replace('\r', r'\r')
            magic_padding = magic_padding.replace('\n', r'\n')
            error += f"{' ' * len(magic_padding)}"
        else:
            ctx_start_idx = 0
        magic_padding = rawline[ctx_start_idx:ctx_end_idx]
        magic_padding = magic_padding.expandtabs(tabsize=4)
        magic_padding = magic_padding.replace('\r', r'\r')
        magic_padding = magic_padding.replace('\n', r'\n')
        error += f"{'~' * len(magic_padding)}^"
        return error

    ## context validate short-cut

    def validate(self) -> CrupyDSLStreamContext:
        """ validate the current context
        """
        return self._stream.context_validate(self)

    ## debug

    def show(self, _indent: int = 0) -> str:
        """ pretty print information
        """
        content  = f"{type(self).__name__}("
        for attr in ['index_start', 'index', 'lineno', 'column']:
            content += f"{attr}={getattr(self, attr)}"
            if attr != 'column':
                content += ','
        return content + ')'
