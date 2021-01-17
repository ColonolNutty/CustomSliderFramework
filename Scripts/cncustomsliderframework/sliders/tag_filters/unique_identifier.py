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


class CSFUniqueIdentifierSliderFilter(CSFSliderTagFilter):
    """ Filter Sliders by their unique identifier.

    .. note:: Using this filter should result in only a single Slider.

    """
    def __init__(self, unique_identifier: str) -> None:
        super().__init__(True, tag_type=CSFSliderTagType.UNIQUE_IDENTIFIER)
        self._unique_identifier = unique_identifier

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[CSFSliderQueryTag]:
        return CSFSliderQueryTag(self.tag_type, self._unique_identifier),

    def __str__(self) -> str:
        return '{}: {}'.format(
            self.__class__.__name__,
            self._unique_identifier
        )
