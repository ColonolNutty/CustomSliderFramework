"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CSFQueryType(CommonInt):
    """ Query types. """
    ALL_PLUS_ANY: 'CSFQueryType' = 0
    ALL_INTERSECT_ANY: 'CSFQueryType' = 1
    ALL_PLUS_ANY_MUST_HAVE_ONE: 'CSFQueryType' = 2
    ALL_INTERSECT_ANY_MUST_HAVE_ONE: 'CSFQueryType' = 3
