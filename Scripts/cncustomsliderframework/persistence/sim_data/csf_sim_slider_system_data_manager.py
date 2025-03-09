"""
DC is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cncustomsliderframework.modinfo import ModInfo
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.persistence.persistence_services.common_persistence_service import CommonPersistenceService
from sims4communitylib.systems.settings.common_settings_data_manager import CommonSettingsDataManager


@CommonDataManagerRegistry.common_data_manager()
class CSFSimSliderSystemDataManager(CommonSettingsDataManager):
    """ Manage a storage of data. """
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_identifier(cls) -> str:
        return 'sim_slider_system_data'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_sim_slider_system_data_manager'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def persistence_services(self) -> Tuple[CommonPersistenceService]:
        from sims4communitylib.persistence.persistence_services.common_file_persistence_service import \
            CommonFilePersistenceService
        result: Tuple[CommonPersistenceService] = (
            CommonFilePersistenceService(per_save=True),
        )
        return result
