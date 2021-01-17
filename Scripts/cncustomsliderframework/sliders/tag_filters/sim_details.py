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
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class CSFSimDetailsSliderFilter(CSFSliderTagFilter):
    """ Filter Sliders by Sim Details. """
    def __init__(self, sim_info: SimInfo) -> None:
        super().__init__(True, tag_type=CSFSliderTagType.SIM_DETAILS)
        self._sim_info = sim_info

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[CSFSliderQueryTag]:
        result: Tuple[CSFSliderQueryTag] = (
            CSFSliderQueryTag(CSFSliderTagType.GENDER, CommonGenderUtils.get_gender(self._sim_info)),
            CSFSliderQueryTag(CSFSliderTagType.AGE, CommonAgeUtils.get_age(self._sim_info)),
            CSFSliderQueryTag(CSFSliderTagType.SPECIES, CommonSpecies.get_species(self._sim_info)),
        )
        return result

    def __str__(self) -> str:
        return '{}: {}, Gender: {}, Age: {}, Species: {}'.format(
            self.__class__.__name__,
            CommonSimNameUtils.get_full_name(self._sim_info),
            CommonGenderUtils.get_gender(self._sim_info),
            CommonAgeUtils.get_age(self._sim_info),
            CommonSpecies.get_species(self._sim_info),
        )
