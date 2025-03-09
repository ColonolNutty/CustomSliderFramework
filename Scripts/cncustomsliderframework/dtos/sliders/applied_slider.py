"""
DC is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict, Any

from sims4communitylib.classes.serialization.common_serializable import CommonSerializable


class CSFAppliedSlider(CommonSerializable):
    """ An appearance Slider that is applied to a Sim. """

    def __init__(
        self,
        slider_name: str,
        slider_value: float
    ):
        self._slider_name = slider_name
        self._slider_value = slider_value

    @property
    def slider_name(self) -> str:
        """The name of the slider."""
        return self._slider_name

    @property
    def slider_value(self) -> float:
        """The value of the slider."""
        return self._slider_value

    @slider_value.setter
    def slider_value(self, value: float):
        self._slider_value = value

    def __repr__(self) -> str:
        return 'name: {}, value: {}'.format(self.slider_name, self.slider_value)

    def __str__(self) -> str:
        return self.__repr__()

    # noinspection PyMissingOrEmptyDocstring
    def serialize(self) -> Union[str, Dict[str, Any]]:
        data = dict()
        data['slider_name'] = self.slider_name
        data['slider_value'] = self._slider_value
        return data

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(cls, data: Union[str, Dict[str, Any]]) -> Union['DCAppliedOverlay', None]:
        slider_name = data.get('slider_name', None)
        if slider_name is None:
            return None
        slider_value = data.get('slider_value', None)
        if slider_value is None or slider_value == 0.0:
            return None

        return cls(
            slider_name,
            slider_value
        )
