"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, List

from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.sliders.slider_loaders.base_slider_loader import CSFBaseSliderLoader
from cncustomsliderframework.tunings.custom_slider_collection import CSFCustomSliderInfoCollection


class CSFCustomSliderFrameworkSliderLoader(CSFBaseSliderLoader):
    """ Loads Custom Slider Framework Sliders. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_slider_loader_custom_slider_framework'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def snippet_names(self) -> Tuple[str]:
        result: Tuple[str] = (
            'custom_slider_info_list',
        )
        return result

    def _load(self, package_slider_info_collection: CSFCustomSliderInfoCollection) -> Tuple[CSFSlider]:
        sliders: List[CSFSlider] = list()
        for package_slider_info in getattr(package_slider_info_collection, 'custom_slider_info_list', tuple()):
            slider = CSFSlider.load_from_package(package_slider_info, self.log)
            if slider is None:
                continue
            sliders.append(slider)
        return tuple(sliders)
