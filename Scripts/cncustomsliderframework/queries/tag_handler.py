"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple


class CSFTagHandler:
    """ A handler for tags. """
    def __init__(self, tag_type: Any):
        self._tag_type = tag_type

    @property
    def tag_type(self) -> Any:
        """ The type of handler. """
        return self._tag_type

    def get_tags(self, script_object: Any) -> Tuple[Any]:
        """ Retrieve tags for this handler. """
        raise NotImplementedError

    # noinspection PyUnusedLocal
    def applies(self, script_object: Any) -> bool:
        """ Determine if this tag handler applies to the object. """
        return True
