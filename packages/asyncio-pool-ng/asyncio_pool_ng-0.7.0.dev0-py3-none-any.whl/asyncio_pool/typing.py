from asyncio import Future
from typing import Any, Protocol, Union

CallbackError = tuple[BaseException, str | None]


class GetResultsHandler(Protocol):
    def __call__(
        self, future: Future
    ) -> Any | BaseException | tuple[Any, None] | tuple[BaseException, None]:
        ...


class AsyncCallbackHandler(Protocol):
    async def __call__(
        self,
        res: Any = None,
        err: CallbackError | None = None,
        ctx: Any = None,
    ) -> Any:
        ...


class SyncCallbackHandler(Protocol):
    def __call__(
        self,
        res: Any = None,
        err: CallbackError | None = None,
        ctx: Any = None,
    ) -> Any:
        ...


CallbackHandler = Union[AsyncCallbackHandler, SyncCallbackHandler]
