"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from cncustomsliderframework.enums.modifier_types import CSFModifierType
from sims.sim_info_types import Age
from sims4.localization import TunableLocalizedString
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import Tunable, TunableList, HasTunableFactory, AutoFactoryInit, TunableEnumSet, TunableSet, \
    TunableEnumEntry
from sims4.tuning.tunable_base import GroupNames
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_species import CommonSpecies
from cncustomsliderframework.enums.slider_category import CSFSliderCategory


class CSFCustomSliderInfo(HasTunableFactory, AutoFactoryInit):
    """ Holds information related to a Custom Slider. """
    FACTORY_TUNABLES = {
        'slider_display_name': TunableLocalizedString(default=None),
        'slider_raw_display_name': Tunable(tunable_type=str, default=None),
        'slider_description': TunableLocalizedString(default=None),
        'slider_author': Tunable(tunable_type=str, default=None),
        'slider_modifier_type': TunableEnumEntry(tunable_type=CSFModifierType, default=CSFModifierType.FACE_MODIFIER),
        'slider_icon_id': Tunable(tunable_type=int, default=0),
        'slider_minimum_value': Tunable(tunable_type=float, default=-100.0),
        'slider_maximum_value': Tunable(tunable_type=float, default=100.0),
        'slider_positive_modifier_id': Tunable(tunable_type=int, default=0),
        'slider_negative_modifier_id': Tunable(tunable_type=int, default=0),
        'available_for_genders': TunableEnumSet(enum_type=CommonGender, default_enum_list=frozenset((CommonGender.MALE, CommonGender.FEMALE))),
        'available_for_ages': TunableEnumSet(enum_type=Age, default_enum_list=frozenset((Age.BABY, Age.TODDLER, Age.CHILD, Age.TEEN, Age.YOUNGADULT, Age.ADULT, Age.ELDER))),
        'available_for_species': TunableEnumSet(enum_type=CommonSpecies, default_enum_list=frozenset((CommonSpecies.HUMAN, CommonSpecies.SMALL_DOG, CommonSpecies.LARGE_DOG, CommonSpecies.CAT))),
        'slider_categories': TunableEnumSet(enum_type=CSFSliderCategory, default_enum_list=frozenset((CSFSliderCategory.OTHER,))),
        'tags': TunableSet(tunable=Tunable(tunable_type=str, default=''), tuning_group=GroupNames.TAG),
    }


class CSFCustomSliderInfoCollection(metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(Types.SNIPPET)):
    """ Holds information related to a collection of custom sliders. """
    INSTANCE_TUNABLES = {
        'custom_slider_info_list': TunableList(tunable=CSFCustomSliderInfo.TunableFactory())
    }
