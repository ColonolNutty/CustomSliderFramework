"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any, Iterator, Tuple

from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class CSFSliderTemplate(HasClassLog):
    """ A template of sliders. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'csf_slider_template'

    @property
    def template_name(self) -> str:
        """The name of the template."""
        return self._template_name

    def __init__(self, template_name: str, slider_to_value_library: Dict[str, float]):
        super().__init__()
        self._template_name = template_name
        self._slider_to_value_library = slider_to_value_library

    def get_sliders(self, sim_info: SimInfo) -> Iterator[Tuple[CSFSlider, float]]:
        """Retrieve sliders associated with this template."""
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        for (identifier, amount) in self._slider_to_value_library.items():
            custom_slider = CSFSliderQueryUtils().locate_by_identifier(identifier)
            if custom_slider is None:
                self.log.debug('No slider found with identifier: {}'.format(identifier))
                continue
            if not custom_slider.is_available_for(sim_info):
                continue
            yield custom_slider, amount

    def apply_to_sim(
        self,
        sim_info: SimInfo
    ) -> bool:
        """Apply the template to a Sim."""
        from cncustomsliderframework.custom_slider_application_service import CSFCustomSliderApplicationService
        slider_application_service = CSFCustomSliderApplicationService()
        for (slider_identifier, amount) in self._slider_to_value_library.items():
            slider_application_service.apply_slider_by_identifier(sim_info, slider_identifier, amount)
        return True

    @classmethod
    def create_from_sim(cls, sim_info: SimInfo, template_name: str) -> 'CSFSliderTemplate':
        """Create a template from a chosen Sim."""
        from cncustomsliderframework.custom_slider_application_service import CSFCustomSliderApplicationService
        slider_application_service = CSFCustomSliderApplicationService()
        slider_to_value_library: Dict[str, float] = dict()
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        for slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            slider_identifier = slider.unique_identifier
            if slider_identifier in slider_to_value_library:
                continue
            slider_value = slider_application_service.get_current_slider_value(sim_info, slider)
            slider_to_value_library[slider_identifier] = slider_value
        return cls(template_name, slider_to_value_library)

    def to_hashable(self) -> Dict[str, Any]:
        """Convert the template into something that is hashable."""
        data = dict()
        data['slider_data'] = self._slider_to_value_library
        return data

    @classmethod
    def from_hashable(cls, template_name: str, data: Dict[str, Any]) -> 'CSFSliderTemplate':
        """Convert the template into something that is hashable."""
        slider_data = data['slider_data']
        return cls(template_name, slider_data)
