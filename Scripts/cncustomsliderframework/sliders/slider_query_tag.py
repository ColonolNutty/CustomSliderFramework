"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from typing import Any, Tuple

from cncustomsliderframework.queries.query_tag import CSFQueryTag
from cncustomsliderframework.sliders.slider_tag_type import CSFSliderTagType


class CSFSliderQueryTag(CSFQueryTag):
    """ A query tag. """
    def __init__(self, tag_type: CSFSliderTagType, value: Any):
        super().__init__(tag_type, value)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def tag_type(self) -> CSFSliderTagType:
        return super().tag_type

    # noinspection PyMissingOrEmptyDocstring
    @property
    def key(self) -> Tuple[CSFSliderTagType, Any]:
        return super().key
