"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cncustomsliderframework.sliders.slider_query_tag import CSFSliderQueryTag
from cncustomsliderframework.sliders.slider_tag_type import CSFSliderTagType
from cncustomsliderframework.sliders.tag_filters.slider_tag_filter import CSFSliderTagFilter


class CSFCustomTagsSliderFilter(CSFSliderTagFilter):
    """ Used to specify tags for filtering. """
    def __init__(self, tags: Tuple[CSFSliderQueryTag], match_all_tags: bool=False, exclude_tags: bool=False):
        super().__init__(match_all_tags, exclude_tags=exclude_tags, tag_type=CSFSliderTagType.CUSTOM_TAG)
        self._custom_tags = tags

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[CSFSliderQueryTag]:
        return self._custom_tags

    def __str__(self) -> str:
        return '{}: {}'.format(
            self.__class__.__name__,
            self._custom_tags
        )
