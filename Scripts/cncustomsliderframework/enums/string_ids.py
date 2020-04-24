"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass


class CSFStringId(Int):
    """ String identifiers used by CSF. """
    CUSTOMIZE_SLIDERS = 3991219124
    CHOOSE_SLIDERS_TO_MODIFY = 2510536869
    RESET_ALL_SLIDERS_NAME = 298545825
    RESET_ALL_SLIDERS_DESCRIPTION = 3476540725
    ARE_YOU_SURE_YOU_WANT_TO_RESET_ALL_SLIDERS = 4271554317
    CONFIRMATION = 2520436614
    # Tokens: {0.String} (Name) {1.String} (Default Val) {2.String} (Min Value) {3.String} (Max Value)
    CHANGE_THE_SLIDER = 3295228480
    # Tokens: {0.String} (Text) {1.String} (Default Val) {2.String} (Min Value) {3.String} (Max Value)
    DEFAULT_MIN_MAX = 3502481568
