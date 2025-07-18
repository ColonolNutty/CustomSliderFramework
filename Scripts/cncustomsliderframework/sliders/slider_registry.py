"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Dict, List, Union

from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.sliders.slider_loaders.base_slider_loader import CSFBaseSliderLoader
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.common_service import CommonService


class CSFSliderRegistry(CommonService, HasLog):
    """ A registry that contains sliders. """
    def __init__(self) -> None:
        super().__init__()
        self._loaded = False
        self.sliders: Dict[str, CSFSlider] = None
        from cncustomsliderframework.sliders.slider_loaders.csf_slider_loader import \
            CSFCustomSliderFrameworkSliderLoader
        self._slider_loaders: List[CSFBaseSliderLoader] = list((
            CSFCustomSliderFrameworkSliderLoader(),
        ))

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_slider_registry'

    @property
    def sliders(self) -> Dict[str, CSFSlider]:
        """A library of sliders organized by their identifiers."""
        if self._sliders is None:
            self.load()
        return self._sliders

    @sliders.setter
    def sliders(self, value: Dict[str, CSFSlider]):
        self._sliders = value

    @property
    def slider_loaders(self) -> List[CSFBaseSliderLoader]:
        """ Loaders that load sliders. """
        return self._slider_loaders

    @classmethod
    def add_loader(
        cls,
        slider_loader: CSFBaseSliderLoader
    ) -> bool:
        """ Add a loader. """
        slider_registry = cls()
        if slider_loader in slider_registry.slider_loaders:
            return False
        slider_registry.slider_loaders.append(slider_loader)
        return True

    def add_slider(self, slider: CSFSlider) -> bool:
        """add_slider(slider)

        Add a Slider to the registry.

        :param slider: An instance of a Slider
        :type slider: CSFSlider
        :return: True, if the slider was successfully added. False, if not.
        :rtype: bool
        """
        unique_id = slider.unique_identifier
        if unique_id in self.sliders:
            return False
        self.sliders[unique_id] = slider
        return True

    def load(self) -> None:
        """ Load data. """
        if self._loaded:
            return
        try:

            sliders_library: Dict[str, CSFSlider] = dict()
            for slider in self._load():
                identifier = slider.unique_identifier
                if identifier in sliders_library:
                    continue
                self._add_additional_slider_data(slider)
                sliders_library[slider.unique_identifier] = slider

            self.sliders = sliders_library
            self._loaded = True
        except Exception as ex:
            self.log.error('Error occurred while loading sliders.', exception=ex)

    def _load(self) -> Iterator[CSFSlider]:
        for slider_loader in self.slider_loaders:
            for slider in slider_loader.load():
                if slider is None:
                    continue
                yield slider

    def _get_sliders(self) -> Iterator[CSFSlider]:
        result: Iterator[CSFSlider] = self.sliders.values()
        return result

    def locate_by_identifier(self, identifier: str) -> Union[CSFSlider, None]:
        """Locate a slider by an identifier."""
        return self.sliders.get(identifier, None)

    # noinspection PyUnusedLocal
    def _add_additional_slider_data(self, slider: CSFSlider) -> None:
        self.log.debug('Adding additional slider data')
        pass


@CommonConsoleCommand(
    ModInfo.get_identity(),
    'csf.show_sliders',
    'Show a list of all sliders.',
)
def _csf_show_sliders(output: CommonConsoleCommandOutput):
    output('Showing loaded Sliders')
    CSFSliderRegistry().log.enable()
    for (unique_id, slider) in CSFSliderRegistry().sliders.items():
        CSFSliderRegistry().log.debug(repr(slider))
    CSFSliderRegistry().log.disable()
    output('Done showing loaded Sliders.')
