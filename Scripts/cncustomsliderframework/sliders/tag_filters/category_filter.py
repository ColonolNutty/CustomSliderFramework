"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cncustomsliderframework.enums.slider_category import CSFSliderCategory
from cncustomsliderframework.sliders.slider_query_tag import CSFSliderQueryTag
from cncustomsliderframework.sliders.slider_tag_type import CSFSliderTagType
from cncustomsliderframework.sliders.tag_filters.slider_tag_filter import CSFSliderTagFilter


class CSFSliderCategorySliderFilter(CSFSliderTagFilter):
    """ Filter Sliders by Category. """
    def __init__(self, slider_category: CSFSliderCategory) -> None:
        super().__init__(True, tag_type=CSFSliderTagType.CATEGORY)
        self._slider_category = slider_category

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[CSFSliderQueryTag]:
        return CSFSliderQueryTag(self.tag_type, self._slider_category),

    def __str__(self) -> str:
        return '{}: {}'.format(
            self.__class__.__name__,
            self._slider_category
        )
