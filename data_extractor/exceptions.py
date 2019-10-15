"""
:mod:`exceptions` -- Extracting Exceptions.
===========================================
"""
# Standard Library
import reprlib

from typing import Any

# Local Folder
from .abc import AbstractExtractors, AbstractSimpleExtractor
from .utils import LazyStr


class ExprError(Exception):
    """
    Invalid Expr.

    :param extractor: The object for data extracting.
    :type extractor: :class:`data_extractor.abc.AbstractSimpleExtractor`
    :param exc: The actual exception is thrown when extracting.
    :type exc: Exception
    """

    def __init__(self, extractor: AbstractSimpleExtractor, exc: Exception):
        self.extractor = extractor
        self.exc = exc

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.extractor!r}, exc={self.exc!r})"


class ExtractError(Exception):
    """
    Thrown by extractor extracting wrong data.

    :param extractor: The object for data extracting.
    :type extractor: :class:`data_extractor.abc.AbstractSimpleExtractor`, \
        :class:`data_extractor.abc.AbstractComplexExtractor`
    :param element: The target data node element.
    :type element: Any
    """

    def __init__(self, extractor: AbstractExtractors, element: Any):
        super().__init__(LazyStr(func=lambda: self._trace_repr))
        self.element = element
        self.extractors = [extractor]

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self.extractors[0]!r}, element={reprlib.repr(self.element)})"
        )

    def _append(self, extractor: AbstractExtractors) -> None:
        self.extractors.append(extractor)

    @property
    def _trace_repr(self) -> str:
        return f"{self.__repr__()}\n" + "\n".join(
            "  " * idx + "|-" + repr(extractor)
            for idx, extractor in enumerate([*self.extractors[::-1], self.element])
        )


__all__ = ("ExprError", "ExtractError")
