"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CSFSliderTagType(CommonInt):
    """ Tag types. """
    ALL: 'CSFSliderTagType' = 0
    SIM_DETAILS: 'CSFSliderTagType' = 1
    GENDER: 'CSFSliderTagType' = 2
    AGE: 'CSFSliderTagType' = 3
    SPECIES: 'CSFSliderTagType' = 4
    CATEGORY: 'CSFSliderTagType' = 5
    CUSTOM_TAG: 'CSFSliderTagType' = 6
    UNIQUE_IDENTIFIER: 'CSFSliderTagType' = 7
    SLIDER_NAME: 'CSFSliderTagType' = 8
