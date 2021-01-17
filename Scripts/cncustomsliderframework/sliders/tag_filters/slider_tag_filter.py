"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union

from cncustomsliderframework.queries.tag_filter import CSFTagFilter
from cncustomsliderframework.sliders.slider_query_tag import CSFSliderQueryTag
from cncustomsliderframework.sliders.slider_tag_type import CSFSliderTagType


class CSFSliderTagFilter(CSFTagFilter):
    """ A filter for use when querying Sliders. """
    def __init__(self, match_all_tags: bool, exclude_tags: bool=False, tag_type: CSFSliderTagType=None):
        super().__init__(match_all_tags, exclude_tags=exclude_tags, tag_type=tag_type)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def tag_type(self) -> Union[CSFSliderTagType, None]:
        return super().tag_type

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[CSFSliderQueryTag]:
        result: Tuple[CSFSliderQueryTag] = super().get_tags()
        return result
