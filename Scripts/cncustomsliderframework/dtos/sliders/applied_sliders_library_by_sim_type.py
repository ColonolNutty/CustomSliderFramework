"""
DC is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict, Any

from cncustomsliderframework.dtos.sliders.applied_sliders_library import CSFAppliedSliderLibrary
from cncustomsliderframework.modinfo import ModInfo
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.enums.sim_type import CommonSimType
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CSFAppliedSliderLibraryBySimType(CommonSerializable, HasClassLog):
    """ A library of sliders applied to a Sim by Sim Type. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'csf_applied_slider_library'

    def __init__(self, applied_sliders_library_by_sim_type: Dict[CommonSimType, CSFAppliedSliderLibrary]):
        super().__init__()
        self._applied_sliders_library_by_sim_type = applied_sliders_library_by_sim_type

    @property
    def applied_sliders_library_by_sim_type(self) -> Dict[CommonSimType, CSFAppliedSliderLibrary]:
        """Applied sliders library by Sim Type."""
        return self._applied_sliders_library_by_sim_type

    # noinspection PyTypeChecker
    @applied_sliders_library_by_sim_type.setter
    def applied_sliders_library_by_sim_type(self, value: Dict[CommonSimType, CSFAppliedSliderLibrary]):
        self._applied_sliders_library_by_sim_type = value

    def has_sim_type(self, sim_type: CommonSimType) -> bool:
        """has_sim_type(sim_type)

        Determine if the library contains selections for a Sim Type.

        :param sim_type: The type of Sim.
        :type sim_type: CommonSimType
        :return: True, if the library contains selections for the specified Sim Type. False, if not.
        :rtype: bool
        """
        return sim_type in self.applied_sliders_library_by_sim_type

    def has_slider_value(self, sim_type: CommonSimType, slider_name: str) -> bool:
        """has_slider_value(sim_type, slider_name)

        Determine if a slider value has been set for a slider.

        :param sim_type: The type of Sim.
        :type sim_type: CommonSimType
        :param slider_name: The name of a Slider.
        :type slider_name: str
        :return: True, if a slider value has been set for a slider. False, if not.
        :rtype: bool
        """
        return self.get_slider_value(sim_type, slider_name) != 0

    def set_slider_value(self, sim_type: CommonSimType, slider_name: str, slider_value: float):
        """set_selected(sim_type, slider_name, slider_value)

        Set the selected part.

        :param sim_type: The type of Sim.
        :type sim_type: CommonSimType
        :param slider_name: The name of a Slider.
        :type slider_name: str
        :param slider_value: The value of the slider.
        :type slider_value: float
        """
        if sim_type not in self.applied_sliders_library_by_sim_type:
            self.applied_sliders_library_by_sim_type[sim_type] = CSFAppliedSliderLibrary(dict())
        self.applied_sliders_library_by_sim_type[sim_type].set_value(slider_name, slider_value)

    def get_slider_value(self, sim_type: CommonSimType, slider_name: str) -> Union[float, None]:
        """get_slider_value(sim_type, slider_name)

        Retrieve the slider value.

        :param sim_type: The type of Sim.
        :type sim_type: CommonSimType
        :param slider_name: The name of a Slider.
        :type slider_name: str
        :return: The slider value or None if no slider value was set.
        :rtype: Union[float]
        """
        library = self.applied_sliders_library_by_sim_type.get(sim_type, None)
        if library is None:
            return None
        return library.get_value(slider_name)

    def get_library(self, sim_type: CommonSimType) -> Union[CSFAppliedSliderLibrary, None]:
        """get_library(sim_type)

        Retrieve the library of Sliders for a Sim Type.

        :param sim_type: The type of Sim.
        :type sim_type: CommonSimType
        :return: The library of Sliders for the specified Sim Type or None if no library is available.
        :rtype: Union[CSFAppliedSliderLibrary, None]
        """
        return self.applied_sliders_library_by_sim_type.get(sim_type, None)

    def clear_slider_value(self, sim_type: CommonSimType, slider_name: str) -> bool:
        """clear_slider_value(sim_type, slider_name)

        Clear a slider.

        :param sim_type: The type of Sim.
        :type sim_type: CommonSimType
        :param slider_name: The name of a Slider.
        :type slider_name: str
        :return: True, if the slider was cleared successfully. False, if not.
        :rtype: bool
        """
        library = self.applied_sliders_library_by_sim_type.get(sim_type, None)
        if library is None:
            return True
        return library.remove_value(slider_name)

    # noinspection PyMissingOrEmptyDocstring
    def serialize(self) -> Union[str, Dict[str, Any]]:
        data = dict()
        for (sim_type, applied_slider_library) in self.applied_sliders_library_by_sim_type.items():
            # noinspection PyBroadException
            try:
                sim_type_name = sim_type.name
            except:
                sim_type_name = str(int(sim_type))
            data[sim_type_name] = applied_slider_library.serialize()
        return data

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(cls, data_library: Union[str, Dict[str, Any]]) -> Union['CSFAppliedSliderLibraryBySimType', None]:
        applied_slider_library_by_sim_type: Dict[Union[int, CommonSimType], CSFAppliedSliderLibrary] = dict()
        try:
            if not data_library:
                cls.get_log().format_with_message('No Applied Slider Data found!', data_library=data_library)
                return cls(applied_slider_library_by_sim_type)
            if isinstance(data_library, dict):
                cls.get_log().format_with_message('Formatting Applied Sliders from data', data_library=data_library)
                for (sim_type_name, applied_slider_library_data) in data_library.items():
                    if sim_type_name is None:
                        continue
                    sim_type = CommonResourceUtils.get_enum_by_name(sim_type_name.upper(), CommonSimType, default_value=None)
                    if sim_type is not None and sim_type == CommonSimType.NONE:
                        continue
                    if sim_type is None:
                        # noinspection PyBroadException
                        try:
                            sim_type = int(sim_type_name)
                        except:
                            continue
                    applied_slider_library = CSFAppliedSliderLibrary.deserialize(applied_slider_library_data)
                    if applied_slider_library is None:
                        continue
                    cls.get_log().format_with_message('Got applied sliders library', sim_type=sim_type, applied_slider_library=applied_slider_library)
                    applied_slider_library_by_sim_type[sim_type] = applied_slider_library
            else:
                cls.get_log().format_with_message('Data Library was not a dictionary!', data_library=data_library)
            return cls(applied_slider_library_by_sim_type)
        except Exception as ex:
            cls.get_log().format_error_with_message('Failed to deserialize Applied Slider data.', data_library=data_library, exception=ex)
        return cls(applied_slider_library_by_sim_type)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return str(self.applied_sliders_library_by_sim_type)
