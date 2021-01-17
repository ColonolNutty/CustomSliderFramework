"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple

from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.queries.tag_handler import CSFTagHandler
from cncustomsliderframework.sliders.slider_tag_type import CSFSliderTagType


class CSFSliderTagHandler(CSFTagHandler):
    """ A filter for Sliders. """
    def __init__(self, tag_type: CSFSliderTagType):
        super().__init__(tag_type)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def tag_type(self) -> CSFSliderTagType:
        return super().tag_type

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self, slider: CSFSlider) -> Tuple[Any]:
        return super().get_tags(slider)

    # noinspection PyMissingOrEmptyDocstring
    def applies(self, slider: CSFSlider) -> bool:
        return super().applies(slider)
