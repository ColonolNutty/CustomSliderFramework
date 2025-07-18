"""
DC is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Union, Dict, Any, List

from cncustomsliderframework.dtos.sliders.applied_slider import CSFAppliedSlider
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable


class CSFAppliedSliderLibrary(CommonSerializable):
    """ A library of sliders applied to a Sim. """

    def __init__(self, sliders: Dict[str, CSFAppliedSlider]):
        self.sliders: Dict[str, CSFAppliedSlider] = sliders

    @property
    def sliders(self) -> Dict[str, CSFAppliedSlider]:
        """Applied sliders."""
        return self._sliders

    @sliders.setter
    def sliders(self, value: Dict[str, CSFAppliedSlider]):
        """Applied sliders."""
        self._sliders = value

    def get_value(self, slider_name: str) -> float:
        """Get a slider value."""
        sliders = self.sliders
        if slider_name in sliders:
            return sliders[slider_name].slider_value
        return 0.0

    def set_value(self, slider_name: str, slider_value: float):
        """Set the value of a slider."""
        sliders = self.sliders
        if slider_name not in sliders:
            applied_slider = CSFAppliedSlider(slider_name, slider_value)
        else:
            applied_slider = sliders[slider_name]
            applied_slider.slider_value = slider_value
        sliders[slider_name] = applied_slider
        self.sliders = sliders

    def remove_value(self, slider_name: str):
        """Remove a slider value."""
        sliders = self.sliders
        if slider_name in sliders:
            del sliders[slider_name]
        self.sliders = sliders

    def __repr__(self) -> str:
        return pformat(self.sliders)

    def __str__(self) -> str:
        return self.__repr__()

    # noinspection PyMissingOrEmptyDocstring
    def serialize(self) -> Union[str, Dict[str, Any]]:
        data = dict()
        serialized_sliders = [slider.serialize() for (slider_name, slider) in self.sliders.items()]
        if serialized_sliders:
            data['sliders'] = serialized_sliders
        return data

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(cls, data: Union[str, Dict[str, Any]]) -> Union['CSFAppliedSliderLibrary', None]:
        sliders_data: List[Dict[str, Any]] = data.get('sliders', list())
        sliders: Dict[str, CSFAppliedSlider] = dict()
        for slider_data in sliders_data:
            slider: CSFAppliedSlider = CSFAppliedSlider.deserialize(slider_data)
            if slider is None:
                continue
            sliders[slider.slider_name] = slider
        return cls(
            sliders
        )
