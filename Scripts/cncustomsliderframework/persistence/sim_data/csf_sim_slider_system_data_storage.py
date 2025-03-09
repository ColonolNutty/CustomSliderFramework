"""
DC is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple, Union

from cncustomsliderframework.dtos.sliders.applied_sliders_library_by_sim_type import CSFAppliedSliderLibraryBySimType
from cncustomsliderframework.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.common_persisted_sim_data_storage import CommonPersistedSimDataStorage
from sims4communitylib.persistence.common_sim_data_storage import _CommonSimDataStorageMetaclass
from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class _CSFSimDataMetaclass(_CommonSimDataStorageMetaclass):
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(mcs) -> CommonModIdentity:
        raise NotImplementedError()

    def __call__(cls, sim_info: SimInfo) -> 'CSFSimSliderSystemData':
        return super(_CSFSimDataMetaclass, cls).__call__(sim_info)


class CSFSimSliderSystemData(CommonPersistedSimDataStorage, metaclass=_CSFSimDataMetaclass):
    """ Sim Slider System Data Storage """

    # noinspection PyMissingOrEmptyDocstring,PyMethodParameters
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'csf_sim_slider_system_data'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_sub_identifier(cls) -> str:
        from cncustomsliderframework.persistence.sim_data.csf_sim_slider_system_data_manager import \
            CSFSimSliderSystemDataManager
        return CSFSimSliderSystemDataManager.get_identifier()

    @property
    def applied_sliders(self) -> CSFAppliedSliderLibraryBySimType:
        """CAS Parts selected for this Sim."""
        if self._applied_sliders is None:
            self._applied_sliders = self.get_data(
                default=CSFAppliedSliderLibraryBySimType(dict()),
                encode=lambda o: o.serialize(),
                decode=lambda o: CSFAppliedSliderLibraryBySimType.deserialize(o)
            )
        return self._applied_sliders

    @applied_sliders.setter
    def applied_sliders(self, value: CSFAppliedSliderLibraryBySimType):
        self._applied_sliders = value
        self.set_data(value, encode=lambda o: o.serialize())

    # noinspection PyMissingOrEmptyDocstring
    @property
    def whitelist_property_names(self) -> Tuple[str]:
        result: Tuple[str, ...] = (
            'sim_name',
            'applied_sliders',
        )
        return result

    def __init__(self, sim_info: SimInfo) -> None:
        self.__data_manager: Union[CommonDataManager, None] = None
        super().__init__(sim_info)
        self._applied_sliders = None

    @property
    def _data_manager(self) -> CommonDataManager:
        if self.__data_manager is None:
            from cncustomsliderframework.persistence.sim_data.csf_sim_slider_system_data_manager import \
                CSFSimSliderSystemDataManager
            self.__data_manager = self._data_manager_registry.locate_data_manager(self.mod_identity, identifier=CSFSimSliderSystemDataManager.get_identifier())
            if self.__data_manager is None:
                raise RuntimeError('Failed to locate a data manager for {} Sim Slider System Data, maybe you forgot to register one?'.format(self.mod_identity.name))
        return self.__data_manager


@CommonConsoleCommand(
    ModInfo.get_identity(),
    'csf.print_sim_slider_system_data',
    'Print Slider System Data for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Name or decimal identifier of a Sim to print data of.', is_optional=True, default_value='Active Sim'),
    ),
    show_with_help_command=False
)
def _csf_command_print_sim_slider_system_data(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    log = CSFSimSliderSystemData.get_log()
    try:
        log.enable()
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        text = f'Sim Slider System Data for Sim: Name: \'{sim_info}\' Id: \'{sim_id}\''
        output(text)
        data_storage = CSFSimSliderSystemData(sim_info)
        for (key, value) in data_storage._data.items():
            sub_text = ' > {}: {}'.format(pformat(key), pformat(value))
            text += sub_text + '\n'
            output(sub_text)
        log.debug(text)
    finally:
        log.disable()
    return True
