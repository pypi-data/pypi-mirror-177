import collections.abc
import typing


class ListViewData(typing.TypedDict):
    data: collections.abc.Sequence[collections.abc.Mapping]
    total: int


class EntryViewData(typing.TypedDict):
    data: collections.abc.Mapping


class LiteralViewData(typing.TypedDict):
    data: typing.Any


class View(typing.Protocol):
    async def __call__(self, *args, **kwargs) -> LiteralViewData | EntryViewData | LiteralViewData: ...
