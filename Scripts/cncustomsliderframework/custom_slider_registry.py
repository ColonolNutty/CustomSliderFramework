"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, List, Union

from cncustomsliderframework.dtos.available_for import CSFAvailableFor
from cncustomsliderframework.dtos.custom_slider import CSFCustomSlider
from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.slider_category import CSFSliderCategory
from cncustomsliderframework.tunings.custom_slider_collection import CSFCustomSliderInfo, CSFCustomSliderInfoCollection
from sims.sim_info import SimInfo
from sims.sim_info_types import Age, Gender
from sims4.resources import Types
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class CSFCustomSliderRegistry(CommonService, HasLog):
    """ Loads CSFCustomSlider from snippet files in packages. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_custom_slider_registry'

    def __init__(self: 'CSFCustomSliderRegistry'):
        super().__init__()
        self._loaded_sliders: List[CSFCustomSlider] = []

    def _load_slider(self, slider_info: CSFCustomSliderInfo) -> Union[CSFCustomSlider, None]:
        display_name: LocalizedString = getattr(slider_info, 'slider_display_name')
        raw_display_name: str = getattr(slider_info, 'slider_raw_display_name')
        if raw_display_name is None:
            self.log.debug('Slider is missing \'slider_raw_display_name\'.')
            return None
        if not display_name:
            display_name = CommonLocalizationUtils.create_localized_string(raw_display_name)
        description: LocalizedString = getattr(slider_info, 'slider_description')
        author: str = str(getattr(slider_info, 'slider_author'))
        icon_id: int = getattr(slider_info, 'slider_icon_id')
        minimum_value: float = getattr(slider_info, 'slider_minimum_value')
        maximum_value: float = getattr(slider_info, 'slider_maximum_value')
        positive_modifier_id: int = getattr(slider_info, 'slider_positive_modifier_id')
        negative_modifier_id: int = getattr(slider_info, 'slider_negative_modifier_id')
        categories: Tuple[CSFSliderCategory] = tuple(getattr(slider_info, 'slider_categories'))
        available_for_genders: Tuple[Gender] = tuple(getattr(slider_info, 'available_for_genders'))
        available_for_ages: Tuple[Age] = tuple(getattr(slider_info, 'available_for_ages'))
        available_for_species: Tuple[CommonSpecies] = tuple(getattr(slider_info, 'available_for_species'))
        available_for = CSFAvailableFor(available_for_genders, available_for_ages, available_for_species)

        custom_slider = CSFCustomSlider(
            display_name,
            raw_display_name,
            description,
            author,
            icon_id,
            available_for,
            categories=categories,
            minimum_value=minimum_value,
            maximum_value=maximum_value,
            positive_modifier_id=positive_modifier_id,
            negative_modifier_id=negative_modifier_id
        )
        self.log.format_with_message('Loading custom slider.', slider=custom_slider)
        if not custom_slider.is_valid():
            self.log.debug('Custom Slider not valid.')
            return None
        self.log.debug('Custom Slider valid.')
        return custom_slider

    def _load_sliders_from_packages_gen(self) -> Iterator[CSFCustomSlider]:
        self.log.debug('Loading sliders from packages.')
        custom_slider_collections: Tuple[CSFCustomSliderInfoCollection] = tuple(CommonResourceUtils.load_instances_with_any_tags(Types.SNIPPET, ('custom_slider_info_list',)))
        for custom_slider_collection in custom_slider_collections:
            custom_slider_info_collection: Tuple[CSFCustomSliderInfo] = tuple(getattr(custom_slider_collection, 'custom_slider_info_list', tuple()))
            for custom_slider_info in custom_slider_info_collection:
                custom_slider = self._load_slider(custom_slider_info)
                if custom_slider is None:
                    continue
                yield custom_slider

    def get_loaded_sliders(self, sim_info: SimInfo) -> Tuple[CSFCustomSlider]:
        """ Retrieve loaded sliders. """
        if self._loaded_sliders is None or len(self._loaded_sliders) == 0:
            self._initialize_registry()
        if sim_info is None:
            return tuple()
        available_sliders: List[CSFCustomSlider] = list()
        for slider in self._loaded_sliders:
            if not slider.is_available_for(sim_info):
                continue
            available_sliders.append(slider)
        return tuple(available_sliders)

    def find_custom_slider_by_name(self, sim_info: SimInfo, name: str) -> Union[CSFCustomSlider, None]:
        """ Locate a custom slider by name. """
        if name is None:
            return None
        for custom_slider in self.get_loaded_sliders(sim_info):
            if custom_slider.raw_display_name is not None and custom_slider.raw_display_name.lower() == name.lower():
                return custom_slider
        return None

    def _initialize_registry(self) -> Tuple[CSFCustomSlider]:
        """ Initialize loaded sliders. """
        self.log.debug('Initializing custom sliders.')
        custom_slider_list = []
        custom_sliders = self._load_sliders_from_packages_gen()
        for custom_slider in custom_sliders:
            custom_slider_list.append(custom_slider)
        self._loaded_sliders = custom_slider_list
        return tuple(custom_slider_list)

    def add_slider(
        self,
        display_name: LocalizedString,
        raw_display_name: str,
        description: LocalizedString,
        author: str,
        icon_id: int,
        available_for: CSFAvailableFor,
        categories: Tuple[CSFSliderCategory]=(CSFSliderCategory.OTHER, ),
        minimum_value: float=-5000.0,
        maximum_value: float=5000.0,
        positive_modifier_id: int=0,
        negative_modifier_id: int=0
    ):
        """ Add a slider to the registry. """
        self._loaded_sliders.append(
            CSFCustomSlider(
                display_name,
                raw_display_name,
                description,
                author,
                icon_id,
                available_for,
                categories=categories,
                minimum_value=minimum_value,
                maximum_value=maximum_value,
                positive_modifier_id=positive_modifier_id,
                negative_modifier_id=negative_modifier_id
            )
        )

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _register_sliders_on_zone_load(event_data: S4CLZoneLateLoadEvent):
        if event_data.game_loaded:
            return
        CSFCustomSliderRegistry.get()._initialize_registry()
