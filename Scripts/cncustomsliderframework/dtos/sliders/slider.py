"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple, List, Union

from sims.sim_info import SimInfo
from protocolbuffers.Localization_pb2 import LocalizedString
from cncustomsliderframework.enums.slider_category import CSFSliderCategory
from cncustomsliderframework.tunings.custom_slider_collection import CSFCustomSliderInfo
from sims4communitylib.classes.calculations.common_available_for_sim import CommonAvailableForSim
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.common_log_registry import CommonLog
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class CSFSlider:
    """ A custom slider. """
    def __init__(
        self,
        display_name: LocalizedString,
        raw_display_name: str,
        description: LocalizedString,
        author: str,
        icon_id: int,
        available_for: CommonAvailableForSim,
        tags: Tuple[str],
        categories: Tuple[CSFSliderCategory]=(CSFSliderCategory.OTHER, ),
        minimum_value: float=-100.0,
        maximum_value: float=100.0,
        positive_modifier_id: int=0,
        negative_modifier_id: int=0,
    ):
        self._display_name = display_name
        self._raw_display_name = raw_display_name
        self._description = description
        self._author = author
        self._icon_id = icon_id
        self._available_for = available_for
        self._categories = categories
        category_names: List[str] = list()
        for slider_category in self.categories:
            if slider_category.name in category_names:
                continue
            category_names.append(slider_category.name)
        self._category_names = tuple(category_names)
        self._minimum_value = minimum_value
        self._maximum_value = maximum_value
        self._positive_modifier_id = positive_modifier_id
        self._negative_modifier_id = negative_modifier_id
        self._unique_identifier = None
        self._tags = tags

    @property
    def unique_identifier(self) -> str:
        """An identifier that identifies the slider in a unique way."""
        if not self._unique_identifier:
            self._unique_identifier = '{}{}{}{}'.format(self.author, self.name, str(self.positive_modifier_id), str(self.negative_modifier_id))
            self._unique_identifier = ''.join((ch for ch in self._unique_identifier if ch.isalnum()))
        return self._unique_identifier

    @property
    def display_name(self) -> LocalizedString:
        """ The string display name of the slider. """
        return self._display_name

    @property
    def display_name_hash(self) -> int:
        """ The display name as hash. """
        return CommonLocalizationUtils.get_localized_string_hash(self.display_name)

    @property
    def raw_display_name(self) -> str:
        """ The raw text display name of the slider. """
        return self._raw_display_name

    @property
    def name(self) -> str:
        """ The name of the slider. """
        return str(self.raw_display_name or self.display_name)

    @property
    def description(self) -> LocalizedString:
        """ The string description of the slider. """
        return self._description

    @property
    def author(self) -> str:
        """ The author of the slider. """
        return self._author

    @property
    def icon_id(self) -> int:
        """ The icon of the slider. """
        return self._icon_id

    @property
    def categories(self) -> Tuple[CSFSliderCategory]:
        """ Categories the slider is a part of. """
        return self._categories

    @property
    def category_names(self) -> Tuple[str]:
        """ The name of the categories the slider is a part of. """
        return self._category_names

    @property
    def minimum_value(self) -> float:
        """ The minimum value of the slider. """
        return self._minimum_value

    @property
    def maximum_value(self) -> float:
        """ The maximum value of the slider. """
        return self._maximum_value

    @property
    def positive_modifier_id(self) -> int:
        """ The positive modifier id of the slider. (When the slider value goes above zero) """
        return self._positive_modifier_id

    @property
    def negative_modifier_id(self) -> int:
        """ The negative modifier id of the slider. (When the slider value goes below zero) """
        return self._negative_modifier_id

    @property
    def available_for(self) -> CommonAvailableForSim:
        """ Availability of the slider. """
        return self._available_for

    @property
    def tags(self) -> Tuple[str]:
        """ Tags of the Slider. """
        return self._tags

    @property
    def tag_list(self) -> Tuple[str]:
        """ A collection of tags for the Slider. """
        tags: List[str] = list()
        tags.append(self.author)
        for gender in self.available_for.genders:
            tags.append(gender.name)
        for part_tag in self.tags:
            tags.append(str(part_tag))
        return tuple(tags)

    def is_available_for(self, sim_info: SimInfo) -> bool:
        """ Determine if available for a Sim. """
        return self.available_for.is_available_for(sim_info)

    def has_positive_modifier_id(self) -> bool:
        """ Determine if this slider has a positive modifier id. """
        return self.positive_modifier_id != 0

    def has_negative_modifier_id(self) -> bool:
        """ Determine if this slider has a negative modifier id. """
        return self.negative_modifier_id != 0

    def get_modifier_ids(self) -> Tuple[int]:
        """ Retrieve a collection of modifier decimal identifiers. """
        modifier_ids: List[int] = list()
        if self.has_positive_modifier_id():
            modifier_ids.append(self.positive_modifier_id)
        if self.has_negative_modifier_id():
            modifier_ids.append(self.negative_modifier_id)
        return tuple(modifier_ids)

    def is_valid(self) -> Tuple[bool, str]:
        """ Determine if the slider is valid or not. """
        if not self.has_positive_modifier_id() and not self.has_negative_modifier_id():
            return False, 'Missing Positive Modifier Id or Negative Modifier Id'
        if self.raw_display_name is None and self.display_name is None:
            return False, 'Missing Raw Display Name or Display Name'
        if self.minimum_value >= self.maximum_value:
            return False, 'Minimum Value is greater than or equal to Maximum Value'
        if not self.available_for.is_valid():
            return False, 'Missing Genders, Ages, and Species of Available For.'
        return True, 'Success'

    def __eq__(self, other: 'CSFSlider') -> bool:
        if not isinstance(other, CSFSlider):
            return False
        return self.positive_modifier_id == other.positive_modifier_id and self.negative_modifier_id == other.negative_modifier_id

    def __hash__(self) -> int:
        return hash((str(self.positive_modifier_id), str(self.negative_modifier_id), self.raw_display_name))

    def __repr__(self) -> str:
        return '<display_name: {}, raw_display_name: {}, author:{}, icon_id {}, minimum_value:{}, maximum_value:{}, positive_modifier_id:{}, negative_modifier_id:{}, available_for: {}>'\
            .format(
                self.display_name,
                self.raw_display_name,
                self.author,
                self.icon_id,
                self.minimum_value,
                self.maximum_value,
                self.positive_modifier_id,
                self.negative_modifier_id,
                pformat(self.available_for)
            )

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def load_from_package(cls, package_slider: CSFCustomSliderInfo, log: CommonLog) -> Union['CSFSlider', None]:
        """load_from_package(package_slider, log)

        Create a slider from a package instance.

        :param package_slider: A package instance.
        :type package_slider: CSFCustomSliderInfo
        :param log: A log to log any errors or warnings to.
        :type log: CommonLog
        :return: The loaded slider.
        :rtype: CSFSlider
        """
        display_name: LocalizedString = getattr(package_slider, 'slider_display_name')
        raw_display_name: str = getattr(package_slider, 'slider_raw_display_name')
        if raw_display_name is None:
            log.warn('Slider is missing Raw Display Name.')
            return None
        if not display_name:
            display_name = CommonLocalizationUtils.create_localized_string(raw_display_name)
        if raw_display_name is None and display_name is None:
            log.warn('Neither a raw display name, nor a display name were specified!')
            return None
        error_display_name = raw_display_name or display_name
        description: LocalizedString = getattr(package_slider, 'slider_description')
        author: str = getattr(package_slider, 'slider_author', None)
        if author is None:
            log.warn('No author was specified for slider \'{}\''.format(error_display_name))
        icon_id: int = getattr(package_slider, 'slider_icon_id', -1)
        minimum_value: float = getattr(package_slider, 'slider_minimum_value', 0.0)
        maximum_value: float = getattr(package_slider, 'slider_maximum_value', 0.0)
        if minimum_value >= maximum_value:
            log.warn('The minimum value was greater than the maximum value for slider \'{}\''.format(error_display_name))
            return None
        positive_modifier_id: int = getattr(package_slider, 'slider_positive_modifier_id', tuple())
        negative_modifier_id: int = getattr(package_slider, 'slider_negative_modifier_id', tuple())
        if positive_modifier_id == 0 and negative_modifier_id == 0:
            log.warn('No positive or negative modifier id specified for slider \'{}\''.format(error_display_name))
            return None
        categories: Tuple[CSFSliderCategory] = getattr(package_slider, 'slider_categories', tuple())
        available_for_genders: Tuple[CommonGender] = tuple(getattr(package_slider, 'available_for_genders', tuple()))
        available_for_ages: Tuple[CommonAge] = tuple([CommonAge.convert_from_vanilla(age) for age in tuple(getattr(package_slider, 'available_for_ages', tuple()))])
        available_for_species: Tuple[CommonSpecies] = tuple(getattr(package_slider, 'available_for_species', tuple()))
        if not available_for_genders and not available_for_ages and not available_for_species:
            log.warn('No Genders, Ages, or Species specified for slider \'{}\''.format(error_display_name))
            return None
        available_for = CommonAvailableForSim(available_for_genders, available_for_ages, available_for_species, (
            CommonOccultType.NON_OCCULT,
            CommonOccultType.ALIEN,
            CommonOccultType.GHOST,
            CommonOccultType.MERMAID,
            CommonOccultType.PLANT_SIM,
            CommonOccultType.ROBOT,
            CommonOccultType.SKELETON,
            CommonOccultType.VAMPIRE,
            CommonOccultType.WITCH
        ))

        tags = tuple(getattr(package_slider, 'tags', tuple()))

        return cls(
            display_name,
            raw_display_name,
            description,
            author,
            icon_id,
            available_for,
            tags,
            categories=categories,
            minimum_value=minimum_value,
            maximum_value=maximum_value,
            positive_modifier_id=positive_modifier_id,
            negative_modifier_id=negative_modifier_id
        )
