"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple

from cncustomsliderframework.dtos.available_for import CSFAvailableFor
from cncustomsliderframework.slider_category import CSFSliderCategory
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo


class CSFCustomSlider:
    """ A custom slider. """
    def __init__(
        self: 'CSFCustomSlider',
        display_name: LocalizedString,
        raw_display_name: str,
        description: LocalizedString,
        author: str,
        icon_id: int,
        available_for: CSFAvailableFor,
        categories: Tuple[CSFSliderCategory]=(CSFSliderCategory.OTHER, ),
        minimum_value: float=-100.0,
        maximum_value: float=100.0,
        positive_modifier_id: int=0,
        negative_modifier_id: int=0
    ):
        self._display_name = display_name
        self._raw_display_name = raw_display_name
        self._description = description
        self._author = author
        self._icon_id = icon_id
        self._available_for = available_for
        self._categories = categories
        self._minimum_value = minimum_value
        self._maximum_value = maximum_value
        self._positive_modifier_id = positive_modifier_id
        self._negative_modifier_id = negative_modifier_id

    @property
    def display_name(self) -> LocalizedString:
        """ The string display name of the slider. """
        return self._display_name

    @property
    def raw_display_name(self) -> str:
        """ The raw text display name of the slider. """
        return self._raw_display_name

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
    def available_for(self) -> CSFAvailableFor:
        """ Availability of the slider. """
        return self._available_for

    def is_available_for(self, sim_info: SimInfo) -> bool:
        """ Determine if available for a Sim. """
        return self.available_for.is_available_for(sim_info)

    def is_valid(self) -> bool:
        """ Determine if the slider is valid or not. """
        return (self.has_positive_modifier_id() or self.has_negative_modifier_id()) and (self.raw_display_name is not None or self.display_name is not None) and self.minimum_value < self.maximum_value and self.available_for.is_valid()

    def has_positive_modifier_id(self) -> bool:
        """ determine if this slider has a positive modifier id. """
        return self.positive_modifier_id != 0

    def has_negative_modifier_id(self) -> bool:
        """ determine if this slider has a negative modifier id. """
        return self.negative_modifier_id != 0

    def __repr__(self) -> str:
        return '<display_name: {}, raw_display_name: {}, author:{}, icon_id {}, minimum_value:{}, maximum_value:{}, positive_modifier_id:{}, negative_modifier_id:{}, available_for: {}>'\
            .format(self.display_name, self.raw_display_name, self.author, self.icon_id, self.minimum_value, self.maximum_value, self.positive_modifier_id, self.negative_modifier_id, pformat(self.available_for))

    def __str__(self) -> str:
        return self.__repr__()
