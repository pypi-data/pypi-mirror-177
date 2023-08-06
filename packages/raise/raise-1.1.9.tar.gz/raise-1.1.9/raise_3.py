# SPDX-License-Identifier: 0BSD
# Copyright 2018 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

"""Raise exceptions with a function instead of a statement.

Provides a minimal, clean and portable interface for raising exceptions
with all the advantages of functions over syntax.
"""

__all__ = ('raise_',)
__version__ = '1.1.9'


def raise_(exception, traceback=None):
    """Raise an exception, optionally with a custom traceback.

    Arguments:
        exception: The exception instance or type to raise.
        traceback (optional): Traceback to raise the exception with.
    """
    if isinstance(exception, type) and issubclass(exception, BaseException):
        exception = exception()
    try:
        exception = exception.with_traceback(traceback)
    except AttributeError:
        pass
    try:
        raise exception
    finally:
        exception = traceback = None
