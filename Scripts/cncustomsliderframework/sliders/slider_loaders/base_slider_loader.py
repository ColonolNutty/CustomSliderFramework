"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator, Any

from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.modinfo import ModInfo
from sims4.resources import Types
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CSFBaseSliderLoader(CommonService, HasLog):
    """ Loads Sliders. """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_slider_loader'

    @property
    def snippet_names(self) -> Tuple[str]:
        """ The names of snippets containing sliders. """
        raise NotImplementedError()

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=tuple())
    def load(self) -> Iterator[CSFSlider]:
        """load()

        Loads all Sliders.

        :return: An iterable of Sliders.
        :rtype: Iterator[CSFSlider]
        """
        snippet_names: Tuple[str] = self.snippet_names

        for snippet_package in CommonResourceUtils.load_instances_with_any_tags(Types.SNIPPET, snippet_names):
            try:
                sliders: Tuple[CSFSlider] = tuple(self._load(snippet_package))

                for slider in sliders:
                    slider: CSFSlider = slider
                    if slider is None:
                        continue
                    (is_valid_result, is_valid_reason) = slider.is_valid()
                    if is_valid_result:
                        yield slider
            except Exception as ex:
                self.log.format_error('Error while parsing sliders from \'{}\''.format(snippet_package), exception=ex)

    def _load(self, package_slider: Any) -> Tuple[CSFSlider]:
        raise NotImplementedError()
