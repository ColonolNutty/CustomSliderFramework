"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CSFStringId(CommonInt):
    """ String identifiers used by CSF. """
    CUSTOMIZE_SLIDERS = 3991219124
    CHOOSE_SLIDERS_TO_MODIFY = 2510536869
    RESET_ALL_SLIDERS_NAME = 298545825
    RESET_ALL_SLIDERS_DESCRIPTION = 3476540725
    ARE_YOU_SURE_YOU_WANT_TO_RESET_ALL_SLIDERS = 4271554317
    CONFIRMATION = 2520436614
    # Tokens: {0.String} (Name)
    CHANGE_THE_SLIDER = 3295228480
    # Tokens: {0.String} (Text) {1.String} (Default Val) {2.String} (Min Value) {3.String} (Max Value)
    DEFAULT_MIN_MAX = 3502481568

    # Tokens: {0.String}
    RANDOMIZE_SLIDER_NAME = 4029355371
    # Tokens: {0.String}
    RANDOMIZE_SLIDER_DESCRIPTION = 645050160
    # Tokens: {0.String}
    RANDOMIZE_SLIDER_CONFIRMATION = 1549399939

    LOADING_SLIDERS = 176561745
    LOADING_SLIDERS_DESCRIPTION = 393250339
    FINISHED_LOADING_SLIDERS = 4219407949
    # Tokens: {0.String} (Num of SLIDERS)
    FINISHED_LOADING_SLIDERS_DESCRIPTION = 3919004570

    SLIDERS_ARE_STILL_LOADING = 1675808145
    # Tokens: {0.String} (FINISHED_LOADING_SLIDERS)
    SLIDERS_ARE_STILL_LOADING_DESCRIPTION = 2361048415

    NO_SLIDERS_FOUND = 886996514
    NO_SLIDERS_FOUND_DESCRIPTION = 1894623033
