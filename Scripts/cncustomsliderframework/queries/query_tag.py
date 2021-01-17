"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple


class CSFQueryTag:
    """ A query tag. """
    def __init__(self, tag_type: Any, value: Any):
        self._tag_type = tag_type
        self._value = value
        self._key = (tag_type, value)

    @property
    def tag_type(self) -> Any:
        """ The tag type. """
        return self._tag_type

    @property
    def value(self) -> Any:
        """ The tag value. """
        return self._value

    @property
    def key(self) -> Tuple[Any, Any]:
        """ The tag represented as a key. """
        return self._key

    def __repr__(self) -> str:
        return str((self.tag_type, self.value))

    def __str__(self) -> str:
        return self.__repr__()
