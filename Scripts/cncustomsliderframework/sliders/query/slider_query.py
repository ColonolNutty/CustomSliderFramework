"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cncustomsliderframework.enums.query_type import CSFQueryType
from cncustomsliderframework.queries.query import CSFQuery
from cncustomsliderframework.sliders.slider_query_tag import CSFSliderQueryTag
from cncustomsliderframework.sliders.tag_filters.slider_tag_filter import CSFSliderTagFilter


class CSFSliderQuery(CSFQuery):
    """ A query used to locate sliders. """
    def __init__(
        self,
        filters: Tuple[CSFSliderTagFilter],
        query_type: CSFQueryType=CSFQueryType.ALL_PLUS_ANY
    ):
        super().__init__(filters, query_type)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def include_all_tags(self) -> Tuple[CSFSliderQueryTag]:
        result: Tuple[CSFSliderQueryTag] = super().include_all_tags
        return result

    # noinspection PyMissingOrEmptyDocstring
    @property
    def include_any_tags(self) -> Tuple[CSFSliderQueryTag]:
        result: Tuple[CSFSliderQueryTag] = super().include_any_tags
        return result

    # noinspection PyMissingOrEmptyDocstring
    @property
    def exclude_tags(self) -> Tuple[CSFSliderQueryTag]:
        result: Tuple[CSFSliderQueryTag] = super().exclude_tags
        return result
