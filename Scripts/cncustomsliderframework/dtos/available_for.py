"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple

from sims.sim_info import SimInfo
from sims.sim_info_types import Age, Gender
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils


class CSFAvailableFor:
    """ Holds information for what types of Sims a thing is available for. """
    def __init__(
        self,
        genders: Tuple[Gender],
        ages: Tuple[Age],
        species: Tuple[CommonSpecies]
    ):
        self._genders = tuple(genders)
        self._ages = tuple(ages)
        self._species = tuple(species)

    @property
    def genders(self) -> Tuple[Gender]:
        """ Genders available. """
        return self._genders

    @property
    def ages(self) -> Tuple[Age]:
        """ Ages available. """
        return self._ages

    @property
    def species(self) -> Tuple[CommonSpecies]:
        """ Species available. """
        return self._species

    def is_available_for(self, sim_info: SimInfo) -> bool:
        """ Determine if available for a Sim. """
        age = CommonAgeUtils.get_age(sim_info)
        if age not in self.ages:
            return False
        gender = CommonGenderUtils.get_gender(sim_info)
        if gender not in self.genders:
            return False
        common_species = CommonSpecies.get_species(sim_info)
        if common_species not in self.species:
            return False
        return True

    def is_valid(self) -> bool:
        """ Determine if available for is valid. """
        return len(self.genders) > 0 or len(self.ages) > 0 or len(self.species) > 0

    def __repr__(self) -> str:
        return '<genders:{}, ages:{}, species:{}>'\
            .format(pformat(self.genders), pformat(self.ages), pformat(self.species))

    def __str__(self) -> str:
        return self.__repr__()
