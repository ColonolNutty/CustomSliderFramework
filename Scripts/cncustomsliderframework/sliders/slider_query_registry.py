"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import collections
from typing import List, Dict, Any, Tuple, Set, Callable

from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.enums.query_type import CSFQueryType
from cncustomsliderframework.enums.string_ids import CSFStringId
from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.sliders.query.slider_query import CSFSliderQuery
from cncustomsliderframework.sliders.query.tag_handlers.slider_tag_handler import CSFSliderTagHandler
from cncustomsliderframework.sliders.slider_tag_type import CSFSliderTagType
from cncustomsliderframework.sliders.tag_filters.slider_tag_filter import CSFSliderTagFilter
from sims4.commands import Command, CheatOutput, CommandType
from sims4communitylib.classes.time.common_stop_watch import CommonStopWatch
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interval.common_interval_event_service import CommonIntervalEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

verbose_log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'csf_slider_query_registry_verbose')


class CSFSliderQueryRegistry(CommonService, HasLog):
    """ Registry handling slider queries. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_slider_query_registry'

    @property
    def _tag_handlers(self) -> List[CSFSliderTagHandler]:
        return self.__tag_handlers

    @property
    def slider_library(self) -> Dict[Tuple[CSFSliderTagType, Any], Set[str]]:
        """ A library of sliders organized by filter keys. """
        return self._slider_library

    @slider_library.setter
    def slider_library(self, value: Dict[Tuple[CSFSliderTagType, Any], Set[str]]):
        self._slider_library = value

    def __init__(self) -> None:
        from cncustomsliderframework.sliders.slider_registry import CSFSliderRegistry
        super().__init__()
        self._collecting = False
        self.slider_library = collections.defaultdict(set)
        self.__tag_handlers: List[CSFSliderTagHandler] = list()
        self._all: List[CSFSlider] = list()
        self._registry = CSFSliderRegistry()

    def add_tag_handler(
        self,
        tag_handler_init: Callable[[CSFSliderTagType], CSFSliderTagHandler],
        tag: CSFSliderTagType
    ):
        """ Add a tag handler. """
        self.__tag_handlers.append(tag_handler_init(tag))

    def create_query(
        self,
        slider_filters: Tuple[CSFSliderTagFilter],
        query_type: CSFQueryType=CSFQueryType.ALL_INTERSECT_ANY_MUST_HAVE_ONE
    ) -> CSFSliderQuery:
        """ Create a query for sliders. """
        return CSFSliderQuery(slider_filters, query_type=query_type)

    def has_sliders(self, queries: Tuple[CSFSliderQuery]) -> bool:
        """ Determine if sliders are available for tags. """
        self.log.format_with_message('Checking if has sliders', queries=queries)
        for _ in self.get_sliders(queries):
            return True
        return False

    def get_all_sliders(self) -> Tuple[CSFSlider]:
        """ Get all sliders. """
        if self._collecting:
            return tuple()
        return tuple(self._all)

    def get_sliders(self, queries: Tuple[CSFSliderQuery]) -> Set[CSFSlider]:
        """ Retrieve sliders matching the queries. """
        self.log.format_with_message('Getting sliders', queries=queries)
        if self._collecting:
            return set()
        sliders = set()
        for query in queries:
            found_sliders = self._query_sliders(query)
            if found_sliders:
                sliders = sliders | found_sliders
        if verbose_log.enabled:
            verbose_log.debug('Finished locating sliders [{}]'.format(',\n'.join(['{}:{}'.format(str(slider.raw_display_name), slider.author) for slider in sliders])))
        return sliders

    def _query_sliders(self, query: CSFSliderQuery) -> Set[CSFSlider]:
        self.log.format_with_message('Querying for sliders using query: {}'.format(query))
        all_tags = query.include_all_tags
        any_tags = query.include_any_tags
        exclude_tags = query.exclude_tags
        found_slider_identifiers = None
        for include_all_tag in all_tags:
            if include_all_tag is None:
                continue
            if include_all_tag.key not in self.slider_library:
                # One of the All keys is not within the slider library! This means no sliders match ALL tags.
                return set()
            new_found_sliders = self.slider_library[include_all_tag.key]
            if found_slider_identifiers is not None:
                self.log.debug('Looking for tag {}'.format(include_all_tag))
                self.log.debug('Before intersect for all_tags {}'.format(len(found_slider_identifiers)))
                new_found_sliders = found_slider_identifiers & new_found_sliders
                self.log.debug('After intersect for all_tags {}'.format(len(new_found_sliders)))
            else:
                self.log.debug('Found with all_tags {}'.format(len(new_found_sliders)))
            found_slider_identifiers = new_found_sliders

        if found_slider_identifiers is None and all_tags:
            self.log.debug('No sliders found for all_tags {}'.format(all_tags))
            return set()

        self.log.debug('After all_tags {}'.format(len(found_slider_identifiers)))
        if verbose_log.enabled:
            found_all_sliders: List[CSFSlider] = list()
            for slider_identifier in found_slider_identifiers:
                slider = self._registry.locate_by_identifier(slider_identifier)
                if slider is None:
                    continue
                found_all_sliders.append(slider)
            verbose_log.format_with_message('Found sliders via all tags', sliders=',\n'.join(['{}:{}'.format(str(found_slider.raw_display_name), found_slider.author) for found_slider in found_all_sliders]))

        found_sliders_via_any_tags = set()
        for include_any_tag in any_tags:
            if include_any_tag is None:
                continue
            if include_any_tag.key not in self.slider_library:
                continue
            found_sliders_via_any_tags = found_sliders_via_any_tags | self.slider_library[include_any_tag.key]

        self.log.debug('Found sliders via any {}'.format(len(found_sliders_via_any_tags)))

        if verbose_log.enabled:
            found_any_sliders: List[CSFSlider] = list()
            for slider_identifier in found_sliders_via_any_tags:
                slider = self._registry.locate_by_identifier(slider_identifier)
                if slider is None:
                    continue
                found_any_sliders.append(slider)
            verbose_log.format_with_message('Found sliders via any tags', sliders=',\n'.join(['{}:{}'.format(str(found_slider.raw_display_name), found_slider.author) for found_slider in found_any_sliders]))

        if found_slider_identifiers is None:
            self.log.debug('No sliders found for all_tags.')
            if not all_tags:
                self.log.debug('Returning any tags.')
                return found_sliders_via_any_tags
        else:
            query_type = query.query_type
            if not any_tags and (query_type == CSFQueryType.ALL_INTERSECT_ANY or query_type == CSFQueryType.ALL_INTERSECT_ANY_MUST_HAVE_ONE):
                query_type = CSFQueryType.ALL_PLUS_ANY
            if query_type == CSFQueryType.ALL_PLUS_ANY:
                found_slider_identifiers = found_slider_identifiers | found_sliders_via_any_tags
            elif query_type == CSFQueryType.ALL_INTERSECT_ANY:
                found_slider_identifiers = found_slider_identifiers & found_sliders_via_any_tags

            if query_type == CSFQueryType.ALL_PLUS_ANY_MUST_HAVE_ONE:
                if not found_sliders_via_any_tags:
                    return set()
                found_slider_identifiers = found_slider_identifiers | found_sliders_via_any_tags
            elif query_type == CSFQueryType.ALL_INTERSECT_ANY_MUST_HAVE_ONE:
                if not found_sliders_via_any_tags:
                    return set()
                found_slider_identifiers = found_slider_identifiers & found_sliders_via_any_tags

        if found_slider_identifiers is None:
            self.log.debug('No found sliders after combining any tags. All Tags: {} Any Tags: {}'.format(all_tags, any_tags))
            return set()

        self.log.debug('After any tags {}'.format(len(found_slider_identifiers)))

        excluded = set()
        for exclude_tag in exclude_tags:
            if exclude_tag is None:
                continue
            if exclude_tag.key not in self.slider_library:
                continue
            excluded = excluded | self.slider_library[exclude_tag.key]

        self.log.debug('Excluding sliders {}'.format(len(excluded)))

        if excluded:
            found_slider_identifiers = found_slider_identifiers - excluded

        self.log.debug('After exclude sliders {}'.format(len(found_slider_identifiers)))
        found_sliders: List[CSFSlider] = list()
        for slider_identifier in found_slider_identifiers:
            slider = self._registry.locate_by_identifier(slider_identifier)
            if slider is None:
                continue
            found_sliders.append(slider)

        if verbose_log.enabled:
            verbose_log.debug('Returning sliders [{}]'.format(',\n'.join(['{}:{}'.format(str(found_slider.raw_display_name), found_slider.author) for found_slider in found_sliders])))
        return set(found_sliders)

    def _organize(self, sliders: Tuple[CSFSlider]):
        self.log.debug('Collecting Sliders Query Data...')
        self.slider_library.clear()
        new_slider_library = dict()
        tag_handlers = tuple(self._tag_handlers)
        for slider in sliders:
            self.log.format_with_message('Handling tags for Slider', cas_part=slider.name)
            slider_identifier = slider.unique_identifier
            slider_tag_keys = list()
            for tag_handler in tag_handlers:
                if not tag_handler.applies(slider):
                    continue
                tag_type = tag_handler.tag_type
                for slider_tag in tag_handler.get_tags(slider):
                    tag_key = (tag_type, slider_tag)
                    slider_tag_keys.append(tag_key)
                    if tag_key not in new_slider_library:
                        new_slider_library[tag_key] = set()
                    if slider_identifier in new_slider_library[tag_key]:
                        continue
                    new_slider_library[tag_key].add(slider_identifier)
            self.log.format_with_message('Applied tags to slider.', display_name=slider.name, keys=slider_tag_keys)

        self.log.format_with_message('Completed collecting Sliders Query Data.', slider_library=new_slider_library)
        self.slider_library = new_slider_library

    def trigger_collection(self, show_loading_notification: bool=True) -> None:
        """trigger_collection(show_loading_notification=True)

        Trigger the action to collect all sliders and organize them by a number of tags.

        :param show_loading_notification: If set to True, the Loading Sliders notification will be shown. If set to False, the Loading Sliders notification will not be shown. Default is True.
        :type show_loading_notification: bool, optional
        """
        def _recollect_data() -> None:
            try:
                if show_loading_notification:
                    CommonBasicNotification(
                        CSFStringId.LOADING_SLIDERS,
                        CSFStringId.LOADING_SLIDERS_DESCRIPTION
                    ).show()
                number_of_sliders = self._collect()
                if number_of_sliders == -1:
                    return
                CommonBasicNotification(
                    CSFStringId.FINISHED_LOADING_SLIDERS,
                    CSFStringId.FINISHED_LOADING_SLIDERS_DESCRIPTION,
                    description_tokens=(str(number_of_sliders),)
                ).show()
            except Exception as ex:
                self.log.error('Error occurred while collecting sliders.', exception=ex)
                self._collecting = False
        _recollect_data()

    def _collect(self) -> int:
        if self._collecting:
            return -1
        self._collecting = True
        try:
            stop_watch = CommonStopWatch()
            stop_watch.start()
            self._all = tuple(self._registry.sliders.values())
            self.log.format_with_message(
                'Loaded Sliders',
                all_list=self._all,
            )
            enabled = self.log.enabled
            self.log.enable()
            self.log.debug('Took {}s to collect {} Sliders.'.format('%.3f' % (stop_watch.stop()), len(self._all)))
            if not enabled:
                self.log.disable()
            stop_watch.start()
            self._organize(self._all)
            self._collecting = False
            self.log.enable()
            self.log.debug('Took {}s to organize Sliders'.format('%.3f' % (stop_watch.stop())))
            if not enabled:
                self.log.disable()
            if self.log.enabled:
                self.log.debug('Loaded {} Sliders.'.format(len(self._all)))
            return len(self._all)
        except Exception as ex:
            self.log.error('Error occurred while collecting Sliders.', exception=ex)
            return -1
        finally:
            self._collecting = False

    @classmethod
    def register_tag_handler(cls, tag_type: CSFSliderTagType) -> Callable[[Any], Any]:
        """ Register a tag handler. """
        def _method_wrapper(tag_handler_callback: Callable[[CSFSliderTagType], CSFSliderTagHandler]):
            cls().add_tag_handler(tag_handler_callback, tag_type)
            return tag_handler_callback
        return _method_wrapper

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _load_sliders_on_zone_load(event_data: S4CLZoneLateLoadEvent):
        if event_data.game_loaded:
            # If the game is already loaded, we've already loaded the data once.
            return False
        CSFSliderQueryRegistry().trigger_collection(show_loading_notification=False)
        return True

    @staticmethod
    @CommonIntervalEventRegistry.run_once(ModInfo.get_identity(), milliseconds=10)
    def _show_sliders_loading_notification_on_first_update() -> None:
        if CSFSliderQueryRegistry()._collecting:
            CommonBasicNotification(
                CSFStringId.LOADING_SLIDERS,
                CSFStringId.LOADING_SLIDERS_DESCRIPTION
            ).show()


@Command('csf.reload_sliders', command_type=CommandType.Live)
def _csf_command_reload_sliders(_connection: int=None):
    output = CheatOutput(_connection)
    output('Reloading Sliders.')
    if CSFSliderQueryRegistry()._collecting:
        output('Failed, Sliders are already being reloaded.')
        return
    CSFSliderQueryRegistry().trigger_collection()
    output('Finished triggering a reload. Now you must wait for the Sliders to finish loading. A notification will appear in the top right of your screen when they are done loading.')
