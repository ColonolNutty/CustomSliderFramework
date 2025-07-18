"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any, Iterator, Tuple, Union

from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.enums.string_ids import CSFStringId
from cncustomsliderframework.modinfo import ModInfo
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class CSFSliderTemplate(HasClassLog):
    """ A template of sliders. """
    _FILE_NAME_REPLACEMENT_CHARACTERS: Dict[str, str] = {
        '<': '_',
        '>': '_',
        ':': '_',
        '"': '_',
        '/': '_',
        '\\': '_',
        '|': '_',
        '?': '_',
        '*': '_'
    }

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

    @property
    def display_name(self) -> LocalizedString:
        """The display name of the template."""
        return self._display_name

    @property
    def source_sim_full_name(self) -> str:
        """The name of the Sim the template was created from."""
        return self._source_sim_full_name

    @property
    def source_sim_age(self) -> CommonAge:
        """The age of the Sim the template was created from."""
        return self._source_sim_age

    @property
    def source_sim_species(self) -> CommonSpecies:
        """The species of the Sim the template was created from."""
        return self._source_sim_species

    @property
    def slider_to_value_library(self) -> Dict[str, float]:
        """A mapping of slider identifiers to their values."""
        return self._slider_to_value_library

    @property
    def template_file_name(self) -> str:
        """The name of the file the template is stored in."""
        template_name = self.template_name
        for (char, replacement) in CSFSliderTemplate._FILE_NAME_REPLACEMENT_CHARACTERS.items():
            template_name = template_name.replace(char, replacement)
        return template_name

    def __init__(
        self,
        template_name: str,
        source_sim_full_name: str,
        source_sim_age: CommonAge,
        source_sim_species: CommonSpecies,
        slider_to_value_library: Dict[str, float]
    ):
        super().__init__()
        self._template_name = template_name
        self._source_sim_full_name = source_sim_full_name
        self._source_sim_age = source_sim_age
        self._source_sim_species = source_sim_species
        self._slider_to_value_library = slider_to_value_library
        self._display_name = CommonLocalizationUtils.create_localized_string(
            CSFStringId.TEMPLATE_DISPLAY_NAME_AGE_SPECIES,
            tokens=(
                template_name,
                source_sim_age.name,
                source_sim_species.name
            )
        )

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
            slider_application_service.apply_slider_by_identifier(sim_info, slider_identifier, amount, trigger_event=True, persist_value=True)
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
            slider_value = slider_application_service.get_current_slider_value(sim_info, slider, use_persisted_value=True)
            slider_to_value_library[slider_identifier] = slider_value
        return cls(
            template_name,
            CommonSimNameUtils.get_full_name(sim_info),
            CommonAge.get_age(sim_info),
            CommonSpecies.get_species(sim_info),
            slider_to_value_library
        )

    def to_hashable(self) -> Dict[str, Any]:
        """Convert the template into something that is hashable."""
        data = dict()
        data['template_name'] = self.template_name
        data['source_sim_name'] = self.source_sim_full_name
        data['source_sim_age'] = self.source_sim_age.name
        data['source_sim_species'] = self.source_sim_species.name
        data['slider_data'] = self.slider_to_value_library
        return data

    @classmethod
    def from_hashable(cls, data: Dict[str, Any]) -> Union['CSFSliderTemplate', None]:
        """Create a template from a library of data."""
        log = cls.get_log()
        template_name = data.get('template_name', None)
        if template_name is None:
            log.error('Missing template name.')
            return None
        source_sim_name = data.get('source_sim_name', None)
        if source_sim_name is None:
            log.format_error_with_message('Missing Source Sim Name.', template_name=template_name)
            return None
        source_sim_age_str = data.get('source_sim_age', None)
        if source_sim_age_str is None:
            log.format_error_with_message('Missing Source Sim Age.', template_name=template_name)
            return None
        source_sim_age = CommonResourceUtils.get_enum_by_name(source_sim_age_str, CommonAge, default_value=CommonAge.INVALID)
        if source_sim_age == CommonAge.INVALID:
            log.format_error_with_message('The Source Sim Age was invalid.', template_name=template_name)
            return None
        source_sim_species_str = data.get('source_sim_species', None)
        if source_sim_species_str is None:
            log.format_error_with_message('Missing Source Sim Species.', template_name=template_name)
            return None
        source_sim_species = CommonResourceUtils.get_enum_by_name(source_sim_species_str, CommonSpecies, default_value=CommonSpecies.INVALID)
        if source_sim_species == CommonSpecies.INVALID:
            log.format_error_with_message('The Source Sim Species was invalid.', template_name=template_name)
            return None
        slider_data = data.get('slider_data', None)
        if slider_data is None:
            log.format_error_with_message('Missing slider data.', template_name=template_name)
            return None
        return cls(
            template_name,
            source_sim_name,
            source_sim_age,
            source_sim_species,
            slider_data
        )
