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

    # Slider Templates
    SLIDER_TEMPLATES_NAME = 3234288887
    SLIDER_TEMPLATES_DESCRIPTION = 72437060
    # Tokens: {0.SimFirstName} {0.SimLastName}
    APPLY_TEMPLATE_TO_SIM_NAME = 2600168760
    APPLY_TEMPLATE_TO_SIM_DESCRIPTION = 1636713932
    # Tokens: {0.SimFirstName} {0.SimLastName}
    APPLY_TEMPLATE_TO_SIM_CONFIRMATION_DESCRIPTION = 2743411501
    # Tokens: {0.String} (Template Name)
    SELECTED_TEMPLATE = 1241474465
    # Tokens: {0.SimFirstName} {0.SimLastName}
    CREATE_TEMPLATE_FROM_SIM_NAME = 502281246
    # Tokens: {0.SimFirstName} {0.SimLastName}
    CREATE_TEMPLATE_FROM_SIM_DESCRIPTION = 368445020

    NO_TEMPLATE_SELECTED = 2034303401
    PLEASE_SELECT_A_TEMPLATE = 2141564348

    ENTER_A_NAME_FOR_YOUR_NEW_TEMPLATE = 1273178247
    TEMPLATE_ALREADY_EXISTS_NAME = 1410843409
    # Tokens: {0.String} (Template Name)
    TEMPLATE_ALREADY_EXISTS_DESCRIPTION = 1393638520
    YES = 979470758
    NO = 1668749452
    VIEW_TEMPLATE_NAME = 1343767120
    VIEW_TEMPLATE_DESCRIPTION = 507219040
    # Tokens: {0.String} {1.String}
    STRING_PLUS_STRING = 1652862138

    NO_TEMPLATES_DETECTED_NAME = 1066846447
    NO_TEMPLATES_DETECTED_DESCRIPTION = 2726384595

    NO_SLIDERS_DETECTED_NAME = 3109711885
    NO_SLIDERS_DETECTED_DESCRIPTION = 3333739470

    # Tokens: {0.String} (Template Name) {1.String} (Age) {2.String} (Species)
    TEMPLATE_DISPLAY_NAME_AGE_SPECIES = 901356426

    REMOVE_SLIDER_CHANGES_NAME = 0x04656943
    REMOVE_SLIDER_CHANGES_DESCRIPTION = 0x974CF0B2

    CHANGE_SLIDER_VALUE_NAME = 0x05722526
    CHANGE_SLIDER_VALUE_DESCRIPTION = 0x7C9B7E53
