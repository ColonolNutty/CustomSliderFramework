"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator, Union

from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.enums.query_type import CSFQueryType
from cncustomsliderframework.enums.slider_category import CSFSliderCategory
from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.sliders.query.slider_query import CSFSliderQuery
from cncustomsliderframework.sliders.tag_filters.category_filter import CSFSliderCategorySliderFilter
from cncustomsliderframework.sliders.tag_filters.sim_details import CSFSimDetailsSliderFilter
from cncustomsliderframework.sliders.tag_filters.slider_name_filter import CSFSliderNameSliderFilter
from cncustomsliderframework.sliders.tag_filters.slider_tag_filter import CSFSliderTagFilter
from cncustomsliderframework.sliders.tag_filters.tags_filter import CSFTagsSliderFilter
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils

from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class CSFSliderQueryUtils(HasLog):
    """ Query for Sliders using various filter configurations. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_slider_utils'

    def __init__(self) -> None:
        super().__init__()
        from cncustomsliderframework.sliders.slider_query_registry import CSFSliderQueryRegistry
        from cncustomsliderframework.sliders.slider_registry import CSFSliderRegistry
        self._query_registry = CSFSliderQueryRegistry()
        self._registry = CSFSliderRegistry()

    def get_all(self) -> Tuple[CSFSlider]:
        """ Get all Sliders. """
        return self._query_registry.get_all_sliders()

    def locate_by_identifier(self, identifier: str) -> Union[CSFSlider, None]:
        """ Locate a Slider by its identifier. """
        return self._registry.locate_by_identifier(identifier)

    def get_sliders_by_name(
        self,
        sim_info: SimInfo,
        name: str,
        ignore_sliders: Tuple[str]=(),
        additional_tags: Tuple[str]=(),
        additional_filters: Iterator[CSFSliderTagFilter]=()
    ) -> Tuple[CSFSlider]:
        """get_sliders_by_name(\
            sim_info,\
            name,\
            ignore_sliders=(),\
            additional_tags=(),\
            additional_filters=()\
        )

        Retrieve Sliders using the criteria.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param name: The name of the sliders to locate.
        :type name: str
        :param additional_tags: Additional tags to add to the query. Default is an empty collection.
        :type additional_tags: Tuple[Any], optional
        :param ignore_sliders: A collection of identifiers to ignore. Default is an empty collection.
        :type ignore_sliders: Tuple[str], optional
        :param additional_filters: Additional filters. Default is an empty collection.
        :type additional_filters: Iterator[CSFSliderTagFilter], optional.
        :return: A collection of Sliders matching the criteria.
        :rtype: Tuple[CSFSlider]
        """
        self.log.format_with_message(
            'Get Sliders by name.',
            name=name,
            additional_filters=tuple(additional_filters),
            ignore_sliders=ignore_sliders,
            additional_tags=additional_tags
        )
        filters: Tuple[CSFSliderTagFilter] = (
            CSFSimDetailsSliderFilter(sim_info),
            CSFSliderNameSliderFilter(name),
            CSFTagsSliderFilter(additional_tags),
            *tuple(additional_filters)
        )
        # Include Object Tag, Include Category Tag

        queries: Tuple[CSFSliderQuery] = (self._query_registry.create_query(filters, query_type=CSFQueryType.ALL_PLUS_ANY),)
        return tuple(self._query_registry.get_sliders(queries))

    def has_sliders_for_sim(
        self,
        sim_info: SimInfo,
        slider_category: CSFSliderCategory=None,
        ignore_sliders: Tuple[str]=(),
        additional_tags: Tuple[str]=(),
        additional_filters: Iterator[CSFSliderTagFilter]=()
    ) -> bool:
        """has_sliders_for_sim(\
            sim_info,\
            slider_category=None,\
            ignore_sliders=(),\
            additional_tags=(),\
            additional_filters=()\
        )

        Determine if Sliders exist for the criteria.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param slider_category: The category of slider. If not specified, sliders will not be filtered by category. Default is None.
        :type slider_category: CSFSliderCategory, optional
        :param additional_tags: Additional tags to add to the query. Default is an empty collection.
        :type additional_tags: Tuple[Any], optional
        :param ignore_sliders: A collection of identifiers to ignore. Default is an empty collection.
        :type ignore_sliders: Tuple[str], optional
        :param additional_filters: Additional filters. Default is an empty collection.
        :type additional_filters: Iterator[CSFSliderTagFilter], optional.
        :return: True, if Sliders exist for the criteria. False, if not.
        :rtype: bool
        """
        self.log.format_with_message(
            'Checking if Sliders exist for Sim.',
            sim_name=CommonSimNameUtils.get_full_name(sim_info),
            slider_category=slider_category,
            additional_filters=additional_filters,
            ignore_sliders=ignore_sliders,
            additional_tags=additional_tags
        )
        filters: Tuple[CSFSliderTagFilter] = (
            CSFSimDetailsSliderFilter(sim_info),
            CSFTagsSliderFilter(additional_tags),
            *additional_filters
        )
        if slider_category is not None:
            filters = (
                *filters,
                CSFSliderCategorySliderFilter(slider_category),
            )
        # Include Object Tag, Include Category Tag

        queries: Tuple[CSFSliderQuery] = (self._query_registry.create_query(filters, query_type=CSFQueryType.ALL_PLUS_ANY),)
        return self._query_registry.has_sliders(queries)

    def get_sliders_for_sim(
        self,
        sim_info: SimInfo,
        slider_category: CSFSliderCategory=None,
        ignore_sliders: Tuple[str]=(),
        additional_tags: Tuple[str]=(),
        additional_filters: Iterator[CSFSliderTagFilter]=()
    ) -> Tuple[CSFSlider]:
        """get_sliders_for_sim(\
            sim_info,\
            slider_category=None,\
            ignore_sliders=(),\
            additional_tags=(),\
            additional_filters=()\
        )

        Retrieve Sliders using the criteria.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param slider_category: The category of slider. If not specified, sliders will not be filtered by category. Default is None.
        :type slider_category: CSFSliderCategory, optional
        :param additional_tags: Additional tags to add to the query. Default is an empty collection.
        :type additional_tags: Tuple[Any], optional
        :param ignore_sliders: A collection of identifiers to ignore. Default is an empty collection.
        :type ignore_sliders: Tuple[str], optional
        :param additional_filters: Additional filters. Default is an empty collection.
        :type additional_filters: Iterator[CSFSliderTagFilter], optional.
        :return: A collection of Sliders matching the criteria.
        :rtype: Tuple[CSFSlider]
        """
        self.log.format_with_message(
            'Get Sliders for Sim.',
            sim_name=CommonSimNameUtils.get_full_name(sim_info),
            slider_category=slider_category,
            additional_filters=tuple(additional_filters),
            ignore_sliders=ignore_sliders,
            additional_tags=additional_tags
        )
        filters: Tuple[CSFSliderTagFilter] = (
            CSFSimDetailsSliderFilter(sim_info),
            CSFTagsSliderFilter(additional_tags),
            *tuple(additional_filters)
        )
        if slider_category is not None:
            filters = (
                *filters,
                CSFSliderCategorySliderFilter(slider_category),
            )
        # Include Object Tag, Include Category Tag

        queries: Tuple[CSFSliderQuery] = (self._query_registry.create_query(filters, query_type=CSFQueryType.ALL_PLUS_ANY),)
        return tuple(self._query_registry.get_sliders(queries))
