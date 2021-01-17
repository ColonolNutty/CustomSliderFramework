"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from Utilities.compiler import compile_module

compile_module(
    root='..\\Release\\CNCustomSliderFramework',
    mod_scripts_folder='.',
    include_folders=('cncustomsliderframework',),
    mod_name='cn_customsliderframework'
)
