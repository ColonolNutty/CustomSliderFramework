"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
from typing import Iterator, Tuple

try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        def __init__(self, val: int):
            pass

        @property
        def name(self) -> str:
            pass

        @property
        def names(self) -> Iterator[str]:
            pass

        @property
        def values(self) -> Iterator[str]:
            pass


class CSFSliderCategory(Int):
    """ Categories for grouping sliders together, """
    OTHER = 0
    FACE = 1
    BODY = 2
    GENITALS = 3

    @staticmethod
    def get_names() -> Tuple[str]:
        """ get_names() """
        return CSFSliderCategory.names
