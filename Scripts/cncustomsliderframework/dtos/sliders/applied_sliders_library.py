"""
DC is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Union, Dict, Any, Iterable, List

from cncustomsliderframework.dtos.sliders.applied_slider import CSFAppliedSlider
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable


class CSFAppliedSliderLibrary(CommonSerializable):
    """ A library of sliders applied to a Sim. """

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

    @property
    def sliders(self) -> Dict[str, CSFAppliedSlider]:
        """Applied sliders."""
        return dict(self._sliders)

    @sliders.setter
    def sliders(self, value: Dict[str, CSFAppliedSlider]):
        """Applied sliders."""
        self._sliders = value

    def get_value(self, slider_name: str) -> float:
        """Get a slider value."""
        if slider_name in self:
            return self[slider_name].slider_value
        return 0.0

    def set_value(self, slider_name: str, slider_value: float):
        """Set the value of a slider."""
        if slider_value == 0.0:
            if slider_name in self:
                del self[slider_name]
        if slider_name not in self.sliders:
            applied_slider = CSFAppliedSlider(slider_name, slider_value)
        else:
            applied_slider = self[slider_name]
            applied_slider.slider_value = slider_value
        self[slider_name] = applied_slider

    def remove_value(self, slider_name: str):
        """Remove a slider value."""
        if slider_name in self:
            del self[slider_name]

    def __init__(self, sliders: Dict[str, CSFAppliedSlider]):
        cleaned_sliders_dict = dict()
        for (slider_name, applied_slider) in sliders.items():
            cleaned_sliders_dict[slider_name] = applied_slider
        self._sliders: Dict[str, CSFAppliedSlider] = cleaned_sliders_dict

    def __iter__(self) -> Iterable[str]:
        for slider in self.sliders.values():
            yield slider

    def __getitem__(self, slider_name: str) -> Union[CSFAppliedSlider, None]:
        return self.sliders.get(slider_name, None)

    def __delitem__(self, slider_name: str):
        sliders = dict(self.sliders)
        del sliders[slider_name]
        self.sliders = sliders

    def __setitem__(self, key: str, value: CSFAppliedSlider):
        sliders = dict(self.sliders)
        sliders[key] = value
        self.sliders = sliders

    def __repr__(self) -> str:
        return pformat(self.sliders)

    def __str__(self) -> str:
        return self.__repr__()
