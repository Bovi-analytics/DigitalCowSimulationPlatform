import csv
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from timeit import Timer
from typing import Any, Callable, Generic, Iterable, Tuple, TypeVar

from numpy import dtype

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

_T = TypeVar("_T")


class AbstractArrayInfo(ABC, Generic[_T]):
    @classmethod
    @abstractmethod
    def shape(cls: Self, array: _T) -> Tuple[int, ...]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def size(cls: Self, array: _T) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def nbytes(cls: Self, array: _T) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def itemsize(cls: Self, array: _T) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def dtype(cls: Self, array: _T) -> dtype:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def count_nonzero(cls: Self, array: _T) -> int:
        raise NotImplementedError

    @classmethod
    def as_tuple(
        cls, array: _T
    ) -> Tuple[Tuple[int, ...], int, int, int, dtype, int]:
        return (
            cls.shape(array),
            cls.size(array),
            cls.nbytes(array),
            cls.itemsize(array),
            cls.dtype(array),
            cls.count_nonzero(array),
        )

    @staticmethod
    def header() -> Tuple[str, ...]:
        return (
            "shape",
            "size",
            "nbytes",
            "itemsize",
            "dtype",
            "count_nonzero",
        )


def timert(stmt: str, setup_func: Callable[..., Any], *args):
    setup_name = setup_func.__name__
    func_name = stmt.__name__
    timer = Timer(
        f"{func_name}(args)",
        f"from __main__ import {setup_name}, {func_name}; args = {setup_name}()",
    )
    timings = timer.repeat(repeat=10, number=10)
    return timings


def csv_writer(
    filename: str,
    # header: Iterable[Any],
    data: Iterable[dict[str:Any]],
    delimiter: str = "\t",
    quotechar: str = '"',
    quoting: int = csv.QUOTE_MINIMAL,
) -> None:
    timestr = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if delimiter == "\t":
        extension = "tsv"
    elif delimiter == ",":
        extension = "csv"
    else:
        extension = "txt"
    output_name = f"{filename}_{timestr}.{extension}"
    with open(output_name, "w", encoding="UTF-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=data[0].keys(),
            delimiter=delimiter,
            quotechar=quotechar,
            quoting=quoting,
        )
        writer.writeheader()
        writer.writerows(data)
