"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple

from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.sliders.query.tag_handlers.slider_tag_handler import CSFSliderTagHandler
from cncustomsliderframework.sliders.slider_query_registry import CSFSliderQueryRegistry
from cncustomsliderframework.sliders.slider_tag_type import CSFSliderTagType


@CSFSliderQueryRegistry.register_tag_handler(tag_type=CSFSliderTagType.ALL)
class CSFAllSliderTagHandler(CSFSliderTagHandler):
    """ Tags. """

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self, slider: CSFSlider) -> Tuple[Any]:
        return 'ALL',
