"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Iterator

from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.events.slider_changed_event import CSFSliderValueChanged
from cncustomsliderframework.modinfo import ModInfo
from protocolbuffers.PersistenceBlobs_pb2 import BlobSimFacialCustomizationData
from sims.sim_info import SimInfo
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService


class CSFCustomSliderApplicationService(CommonService, HasLog):
    """ Change and Reset Custom Sliders. """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_slider_application_service'

    def _get_facial_attributes(self, sim_info: SimInfo) -> BlobSimFacialCustomizationData:
        facial_attributes = BlobSimFacialCustomizationData()
        # noinspection PyPropertyAccess
        facial_attributes.MergeFromString(sim_info.facial_attributes)
        return facial_attributes

    def _set_facial_attributes(self, sim_info: SimInfo, new_facial_attributes: BlobSimFacialCustomizationData):
        sim_info.facial_attributes = new_facial_attributes.SerializeToString()
        sim_info.resend_facial_attributes()

    def _get_existing_modifiers_for_edit(
        self,
        sim_info: SimInfo,
        exclude_facial_modifier_ids: Iterator[int]=(),
        exclude_body_modifier_ids: Iterator[int]=(),
        exclude_sculpt_ids: Iterator[int]=()
    ) -> BlobSimFacialCustomizationData:
        facial_attributes = self._get_facial_attributes(sim_info)
        existing_modifiers = BlobSimFacialCustomizationData()

        self.log.debug('Adding face modifiers.')
        # noinspection PyUnresolvedReferences
        for face_modifier in facial_attributes.face_modifiers:
            # Exclude the opposite modifier so it no longer applies.
            if face_modifier.key in exclude_facial_modifier_ids:
                self.log.debug('Excluding face modifier with key {}'.format(face_modifier.key))
                continue
            # noinspection PyUnresolvedReferences
            existing_modifiers.face_modifiers.append(face_modifier)

        self.log.debug('Adding body modifiers.')
        # noinspection PyUnresolvedReferences
        for body_modifier in facial_attributes.body_modifiers:
            if body_modifier.key in exclude_body_modifier_ids:
                continue
            # noinspection PyUnresolvedReferences
            existing_modifiers.body_modifiers.append(body_modifier)

        self.log.debug('Adding sculpt modifiers.')
        # noinspection PyUnresolvedReferences
        for sculpt in facial_attributes.sculpts:
            sculpt: int = sculpt
            if sculpt in exclude_sculpt_ids:
                self.log.debug('Excluding sculpt with id {}'.format(sculpt))
                continue
            # noinspection PyUnresolvedReferences
            existing_modifiers.sculpts.append(sculpt)
        return existing_modifiers

    def get_current_slider_value_by_identifier(self, sim_info: SimInfo, identifier: str) -> float:
        """ Retrieve the current value of a slider by its identifier. """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        custom_slider = CSFSliderQueryUtils().locate_by_identifier(identifier)
        if custom_slider is None:
            self.log.debug('No slider found with identifier: {}'.format(identifier))
            return False
        return self.get_current_slider_value(sim_info, custom_slider)

    def get_current_slider_value_by_name(self, sim_info: SimInfo, slider_name: str) -> float:
        """ Retrieve the current value of a slider by its name. """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        custom_sliders = CSFSliderQueryUtils().get_sliders_by_name(sim_info, slider_name)
        if not custom_sliders:
            self.log.debug('No sliders found with name: {}'.format(slider_name))
            return False
        custom_slider = next(iter(custom_sliders))
        if custom_slider is None:
            self.log.debug('No slider found with name: {}'.format(slider_name))
            return False
        return self.get_current_slider_value(sim_info, custom_slider)

    def get_current_slider_value(self, sim_info: SimInfo, custom_slider: CSFSlider) -> float:
        """ Retrieve the current value of a slider. """
        if sim_info is None or custom_slider is None:
            return False
        facial_attributes = self._get_facial_attributes(sim_info)

        # noinspection PyUnresolvedReferences
        for face_modifier in facial_attributes.face_modifiers:
            if face_modifier.amount == 0.0:
                continue
            if custom_slider.has_negative_modifier_id() and face_modifier.key == custom_slider.negative_modifier_id:
                self.log.debug('Found existing negative face modifier value {} with key {}'.format(face_modifier.amount, face_modifier.key))
                return (face_modifier.amount * -1.0)/0.01
            if custom_slider.has_positive_modifier_id() and face_modifier.key == custom_slider.positive_modifier_id:
                self.log.debug('Found existing positive face modifier value {} with key {}'.format(face_modifier.amount, face_modifier.key))
                return face_modifier.amount/0.01

        # noinspection PyUnresolvedReferences
        for body_modifier in facial_attributes.body_modifiers:
            if body_modifier.amount == 0.0:
                continue
            if custom_slider.has_negative_modifier_id() and body_modifier.key == custom_slider.negative_modifier_id:
                self.log.debug('Found existing negative body modifier modifier value {} with key {}'.format(body_modifier.amount, body_modifier.key))
                return (body_modifier.amount * -1.0)/0.01
            if custom_slider.has_positive_modifier_id() and body_modifier.key == custom_slider.positive_modifier_id:
                self.log.debug('Found existing positive body modifier value {} with key {}'.format(body_modifier.amount, body_modifier.key))
                return body_modifier.amount/0.01
        return 0.0

    def apply_slider(self, sim_info: SimInfo, custom_slider: CSFSlider, amount: float, trigger_event: bool=False) -> bool:
        """ Apply a slider to a Sim. """
        try:
            if sim_info is None or custom_slider is None:
                self.log.debug('Missing sim_info or custom_slider')
                return False

            if not custom_slider.is_available_for(sim_info):
                self.log.format_with_message('The specified slider is not available for the Sim.', sim=sim_info, slider=custom_slider)
                return False

            self.log.debug('Determining which slider to use for {} with amount {}.'.format(custom_slider.raw_display_name, amount))
            if amount >= 0:
                self.log.debug('Amount is greater than or equal to 0.0. It is {}.'.format(amount))
                if not custom_slider.has_positive_modifier_id():
                    self.log.debug('No positive modifier id.')
                    return False
                self.log.debug('Has positive modifier id.')
                slider_amount = amount * 0.01
                slider_id = custom_slider.positive_modifier_id
            else:
                self.log.debug('Amount is less than zero. It is {}.'.format(amount))
                if not custom_slider.has_negative_modifier_id():
                    self.log.debug('No negative modifier id.')
                    return False
                self.log.debug('Has negative modifier id.')
                slider_amount = amount * -0.01
                slider_id = custom_slider.negative_modifier_id

            if slider_id == 0:
                self.log.error('Slider key is zero!')
                return False

            current_slider_amount = self.get_current_slider_value(sim_info, custom_slider)

            self.log.debug('Applying facial attribute.')
            modified_facial_attributes = self._get_existing_modifiers_for_edit(sim_info, exclude_facial_modifier_ids=(*custom_slider.get_modifier_ids(), slider_id))

            if slider_amount > 0.0 or slider_amount == custom_slider.minimum_value or slider_amount == custom_slider.maximum_value:
                self.log.debug('Adding the custom slider because the amount is greater than zero.')
                new_modifier = BlobSimFacialCustomizationData().Modifier()
                new_modifier.key = slider_id
                new_modifier.amount = slider_amount
                # noinspection PyUnresolvedReferences
                modified_facial_attributes.face_modifiers.append(new_modifier)
            else:
                self.log.debug('Excluding the custom slider because the amount is zero.')
            self._set_facial_attributes(sim_info, modified_facial_attributes)
            if trigger_event:
                from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
                CommonEventRegistry().dispatch(CSFSliderValueChanged(sim_info, custom_slider, current_slider_amount, slider_amount))
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while applying slider: \'{}\''.format(custom_slider.raw_display_name), exception=ex)

    def apply_slider_by_name(self, sim_info: SimInfo, name: str, amount: float) -> bool:
        """ Apply a slider with its name. """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        self.log.debug('Attempting to apply slider with name {} and amount {}'.format(name, amount))
        custom_sliders = CSFSliderQueryUtils().get_sliders_by_name(sim_info, name)
        if not custom_sliders:
            self.log.debug('No sliders found with name: {}'.format(name))
            return False
        custom_slider = next(iter(custom_sliders))
        if custom_slider is None:
            self.log.debug('No slider found with name: {}'.format(name))
            return False
        self.log.debug('Slider found, attempting to apply.')
        return self.apply_slider(sim_info, custom_slider, amount)

    def apply_slider_by_identifier(self, sim_info: SimInfo, identifier: str, amount: float) -> bool:
        """ Apply a slider with its identifier. """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        self.log.debug('Attempting to apply slider with identifier {} and amount {}'.format(identifier, amount))
        custom_slider = CSFSliderQueryUtils().locate_by_identifier(identifier)
        if custom_slider is None:
            self.log.debug('No slider found with identifier: {}'.format(identifier))
            return False
        self.log.debug('Slider found, attempting to apply.')
        return self.apply_slider(sim_info, custom_slider, amount)

    def apply_random(self, sim_info: SimInfo, custom_slider: CSFSlider) -> bool:
        """ Apply a random value for a slider. """
        name = custom_slider.raw_display_name
        amount = random.randint(int(custom_slider.minimum_value), int(custom_slider.maximum_value))
        self.log.debug('Attempting to apply slider with name {} and amount {}'.format(name, amount))
        return self.apply_slider(sim_info, custom_slider, amount)

    def reset_slider(self, sim_info: SimInfo, custom_slider: CSFSlider) -> bool:
        """ Reset a Slider to its default for a Sim. """
        return self.apply_slider(sim_info, custom_slider, 0.0)

    def reset_all_sliders(self, sim_info: SimInfo) -> bool:
        """ Reset all Custom Sliders for a Sim. """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        for custom_slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            self.reset_slider(sim_info, custom_slider)
        return True
