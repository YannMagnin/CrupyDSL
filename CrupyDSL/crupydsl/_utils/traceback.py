"""
crupydsl._utils.traceback   - traceback magic
"""
__all__ = [
    'crupy_traceback_find',
]
import sys
import traceback

#---
# Internals
#---

def __clean_filename(filename: str) -> str:
    """ try to remove virtualenv prefix if detected
    """
    for prefix in sys.path:
        if filename.startswith(prefix):
            return f"<venv>:{filename[len(prefix)+1:]}"
    return filename

def __find_traceback() -> traceback.FrameSummary:
    """ try to skip unwanted frame
    """
    _, _, tb = sys.exc_info()
    tb_info = traceback.extract_tb(tb)
    for i in range(0, len(tb_info)):
        if tb_info[-1 - i][0].find('crupydsl/_utils') < 0:
            return tb_info[-1 - i]
    return tb_info[-1]

#---
# Public
#---

def crupy_traceback_find() -> str:
    """ try to find last exeption information

    @notes
    - skip unwanted traceback frame
    - remove venv path prefix
    """
    filename, line, func, text = __find_traceback()
    filename = __clean_filename(filename)
    exec_info  = f"An error occurred on line \"{filename}::{func}<{line}> "
    exec_info += f"-> `{text}`\""
    return exec_info
