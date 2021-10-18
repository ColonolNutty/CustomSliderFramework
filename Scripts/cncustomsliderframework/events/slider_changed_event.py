"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent


class CSFSliderValueChanged(CommonEvent):
    """An event that occurs when a slider value has been changed on a Sim."""

    def __init__(self, sim_info: SimInfo, slider: CSFSlider, old_value: float, new_value: float):
        self._sim_info = sim_info
        self._slider = slider
        self._old_value = old_value
        self._new_value = new_value

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that changed."""
        return self._sim_info

    @property
    def slider_name(self) -> str:
        """The name of the slider that changed."""
        return self.slider.raw_display_name

    @property
    def slider(self) -> CSFSlider:
        """The slider that changed."""
        return self._slider

    @property
    def old_value(self) -> float:
        """The value the slider was at before the change."""
        return self._old_value

    @property
    def new_value(self) -> float:
        """The value the slider is now at."""
        return self._new_value
