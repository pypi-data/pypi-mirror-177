from asyncio import Future
from functools import partial

from .typing import GetResultsHandler


def result_noraise(future: Future, flat: bool = True):
    """Extracts result from future, never raising an exception.

    If `flat` is True -- returns result or exception instance (including
    CancelledError), if `flat` is False -- returns tuple of (`result`,
    `exception` object).

    If traceback is needed -- just re-raise returned exception."""
    try:
        res = future.result()
        return res if flat else (res, None)
    except BaseException as exc:
        return exc if flat else (None, exc)


class getres:
    dont: GetResultsHandler = lambda fut: fut
    flat: GetResultsHandler = partial(result_noraise, flat=True)
    pair: GetResultsHandler = partial(result_noraise, flat=False)
