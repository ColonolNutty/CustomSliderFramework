"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Dict, Any, Union

from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.slider_templates.slider_template import CSFSliderTemplate
from sims.sim_info import SimInfo
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_json_io_utils import CommonJSONIOUtils


class CSFSliderTemplateUtils(CommonService, HasLog):
    """ Utilities for slider templates. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_slider_template_utils'

    def __init__(self) -> None:
        super().__init__()
        self._template_library: Dict[str, CSFSliderTemplate] = None

    @property
    def template_library(self) -> Dict[str, CSFSliderTemplate]:
        """ A library of templates organized by their name. """
        if self._template_library is None:
            self._template_library = self._load()
        return self._template_library

    def get_template_by_name(self, template_name: str) -> Union[CSFSliderTemplate, None]:
        """Locate a template by its name."""
        return self.template_library.get(template_name, None)

    def apply_template_to_sim_by_name(
        self,
        sim_info: SimInfo,
        template_name: str
    ) -> bool:
        """Apply a template to a Sim by its name."""
        template = self.get_template_by_name(template_name)
        if template is None:
            return False
        return template.apply_to_sim(sim_info)

    def save_sliders_of(
        self,
        sim_info: SimInfo,
        template_name: str
    ) -> bool:
        """Save sliders applied to a Sim."""
        template = CSFSliderTemplate.create_from_sim(sim_info, template_name)
        if template is None:
            return False
        self.template_library[template_name] = template
        self.save_template(template)
        return True

    def save_template(self, template: CSFSliderTemplate, folder_path: str=None) -> bool:
        """Save templates."""
        if folder_path is None:
            folder_path = self._folder_path()
            os.makedirs(folder_path, exist_ok=True)

        template_file_name = template.template_file_name
        template_file_path = os.path.join(folder_path, '{}.json'.format(template_file_name))
        if os.path.exists(template_file_path):
            os.remove(template_file_path)

        self.log.format_with_message('Saving template.', template_file_name=template_file_name)
        template: CSFSliderTemplate = template
        return CommonJSONIOUtils.write_to_file(template_file_path, template.to_hashable())

    def save_templates(self) -> bool:
        """Save templates."""
        folder_path = self._folder_path()
        os.makedirs(folder_path, exist_ok=True)
        for (template_name, template) in self.template_library.items():
            template: CSFSliderTemplate = template
            self.save_template(template, folder_path=folder_path)
        return True

    def _load(self) -> Dict[str, 'CSFSliderTemplate']:
        folder_path = self._folder_path()
        if not os.path.exists(folder_path):
            self.log.format_with_message('No folder was found at path.', folder_path=folder_path)
            return dict()

        loaded_data: Dict[str, Dict[str, Any]] = CommonJSONIOUtils.load_from_folder(folder_path)
        if not loaded_data:
            return dict()

        template_library = dict()
        for (template_file_name, template_data) in loaded_data.items():
            template = CSFSliderTemplate.from_hashable(template_data)
            if template is None:
                self.log.format_with_message('Failed to load template', template_file_name=template_file_name)
                continue
            template_library[template.template_name] = template
        return template_library

    def _folder_path(self) -> str:
        from sims4communitylib.persistence.persistence_services.common_folder_persistence_service import \
            CommonFolderPersistenceService
        folder_persistence_service = CommonFolderPersistenceService()
        return folder_persistence_service._folder_path(self.mod_identity, identifier='slider_templates')
