"""
DC is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any, Union

from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.persistence.sim_data.csf_sim_slider_system_data_manager import \
    CSFSimSliderSystemDataManager
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_log_registry import CommonLogRegistry


class CSFSimSliderSystemDataManagerUtils(CommonService):
    """ Utilities for accessing Sim Slider System Data stores """
    def __init__(self) -> None:
        self._data_manager: Union[CSFSimSliderSystemDataManager, None] = None

    @property
    def data_manager(self) -> CSFSimSliderSystemDataManager:
        """ The data manager containing data. """
        if self._data_manager is None:
            # noinspection PyTypeChecker
            self._data_manager: CSFSimSliderSystemDataManager = CommonDataManagerRegistry().locate_data_manager(ModInfo.get_identity(), identifier=CSFSimSliderSystemDataManager.get_identifier())
        return self._data_manager

    def get_all_data(self) -> Dict[str, Dict[str, Any]]:
        """ Get all data. """
        return self.data_manager._data_store_data

    def save(self) -> bool:
        """ Save data. """
        return self.data_manager.save()

    def reset(self, prevent_save: bool = False) -> bool:
        """ Reset data. """
        return self.data_manager.remove_all_data(prevent_save=prevent_save)


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'csf.print_mod_sim_slider_system_data')


@CommonConsoleCommand(ModInfo.get_identity(), 'csf.print_mod_sim_slider_system_data', 'Print slider system data.', show_with_help_command=False)
def _csf_command_print_mod_sim_slider_system_data(output: CommonConsoleCommandOutput):
    output('Printing CSF Mod Sim Slider System Data to Messages.txt file. This may take a little bit, be patient.')
    log.enable()
    log.format(data_store_data=CSFSimSliderSystemDataManagerUtils().get_all_data())
    log.disable()
    return True


@CommonConsoleCommand(ModInfo.get_identity(), 'csf.clear_mod_sim_slider_system_data', 'Clear slider system data', show_with_help_command=False)
def _csf_command_clear_mod_sim_slider_system_data(output: CommonConsoleCommandOutput):
    output('Clearing CSF Mod Sim Slider System Data.')
    CSFSimSliderSystemDataManagerUtils().reset(prevent_save=True)
    from cncustomsliderframework.persistence.sim_data.csf_sim_slider_system_data_storage import CSFSimSliderSystemData
    CSFSimSliderSystemData.clear_instances(ModInfo.get_identity())
    output('!!! PLEASE READ !!!')
    output('Sim Slider System Data Cleared. Ensure you save your game!')
    output('!!!!!!!!!!!!!!!!!!!')
    return True
