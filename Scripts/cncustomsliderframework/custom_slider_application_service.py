"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Iterator, Union

from cncustomsliderframework.dtos.sliders.applied_slider import CSFAppliedSlider
from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.events.slider_changed_event import CSFSliderValueChanged
from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.persistence.sim_data.csf_sim_slider_system_data_storage import CSFSimSliderSystemData
from protocolbuffers.PersistenceBlobs_pb2 import BlobSimFacialCustomizationData
from sims.sim_info import SimInfo
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils


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

    def reapply_all_sliders(self, sim_info: SimInfo):
        """Reapply all sliders on a Sim."""
        sim_data = CSFSimSliderSystemData(sim_info)
        current_sim_type = CommonSimTypeUtils.determine_sim_type(sim_info, use_current_occult_type=True)
        slider_library = sim_data.applied_sliders.get_library(current_sim_type)
        if slider_library is None:
            return
        for slider in slider_library.sliders.values():
            slider: CSFAppliedSlider = slider
            self.apply_slider_by_name(sim_info, slider.slider_name, slider.slider_value, trigger_event=True, persist_value=False)

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
        exclude_modifier_ids: Iterator[int] = ()
    ) -> BlobSimFacialCustomizationData:
        facial_attributes = self._get_facial_attributes(sim_info)
        existing_modifiers = BlobSimFacialCustomizationData()

        self.log.debug('Adding face modifiers.')
        # noinspection PyUnresolvedReferences
        for face_modifier in facial_attributes.face_modifiers:
            # Exclude the opposite modifier so it no longer applies.
            if face_modifier.key in exclude_modifier_ids:
                self.log.debug(f'Excluding face modifier with key {face_modifier.key}')
                continue
            # noinspection PyUnresolvedReferences
            existing_modifiers.face_modifiers.append(face_modifier)

        self.log.debug('Adding aged face modifiers.')
        # noinspection PyUnresolvedReferences
        for aged_face_modifier in facial_attributes.aged_face_modifiers:
            # Exclude the opposite modifier so it no longer applies.
            if aged_face_modifier.key in exclude_modifier_ids:
                self.log.debug(f'Excluding aged face modifier with key {aged_face_modifier.key}')
                continue
            # noinspection PyUnresolvedReferences
            existing_modifiers.aged_face_modifiers.append(aged_face_modifier)

        self.log.debug('Adding body modifiers.')
        # noinspection PyUnresolvedReferences
        for body_modifier in facial_attributes.body_modifiers:
            if body_modifier.key in exclude_modifier_ids:
                self.log.debug(f'Excluding body modifier with key {body_modifier.key}')
                continue
            # noinspection PyUnresolvedReferences
            existing_modifiers.body_modifiers.append(body_modifier)

        self.log.debug('Adding aged body modifiers.')
        # noinspection PyUnresolvedReferences
        for aged_body_modifier in facial_attributes.aged_body_modifiers:
            if aged_body_modifier.key in exclude_modifier_ids:
                self.log.debug(f'Excluding aged body modifier with key {aged_body_modifier.key}')
                continue
            # noinspection PyUnresolvedReferences
            existing_modifiers.aged_body_modifiers.append(aged_body_modifier)

        self.log.debug('Adding sculpt modifiers.')
        # noinspection PyUnresolvedReferences
        for sculpt in facial_attributes.sculpts:
            sculpt: int = sculpt
            # noinspection PyUnresolvedReferences
            existing_modifiers.sculpts.append(sculpt)
        return existing_modifiers

    def get_current_slider_value_by_identifier(self, sim_info: SimInfo, identifier: str, use_persisted_value: bool = False, **__) -> Union[float, None]:
        """get_current_slider_value_by_identifier(sim_info, identifier, use_persisted_value=True)

        Retrieve the current value of a slider by its identifier.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param identifier: The identifier of a slider.
        :type identifier: str
        :param use_persisted_value: If True, the persisted value will be used rather than the current value on the Sim. If False, the current value on the Sim will be used. Default is True.
        :type use_persisted_value: bool, optional
        :return: The current slider value for the slider or None if the slider does not exist.
        :rtype: Union[float, None]
        """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        custom_slider = CSFSliderQueryUtils().locate_by_identifier(identifier)
        if custom_slider is None:
            self.log.debug(f'No slider found with identifier: {identifier}')
            return None
        return self.get_current_slider_value(sim_info, custom_slider, use_persisted_value=use_persisted_value)

    def get_current_slider_value_by_name(self, sim_info: SimInfo, slider_name: str, use_persisted_value: bool = False, **__) -> Union[float, None]:
        """get_current_slider_value_by_identifier(sim_info, slider_name, use_persisted_value=True)

        Retrieve the current value of a slider by its name.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param slider_name: The name of a slider.
        :type slider_name: str
        :param use_persisted_value: If True, the persisted value will be used rather than the current value on the Sim. If False, the current value on the Sim will be used. Default is True.
        :type use_persisted_value: bool, optional
        :return: The current slider value for the slider or None if the slider does not exist.
        :rtype: Union[float, None]
        """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        custom_sliders = CSFSliderQueryUtils().get_sliders_by_name(sim_info, slider_name)
        if not custom_sliders:
            self.log.debug(f'No sliders found with name: {slider_name}')
            return None
        custom_slider = next(iter(custom_sliders))
        if custom_slider is None:
            self.log.debug(f'No slider found with name: {slider_name}')
            return None
        return self.get_current_slider_value(sim_info, custom_slider, use_persisted_value=use_persisted_value)

    def get_current_slider_value(self, sim_info: SimInfo, custom_slider: CSFSlider, use_persisted_value: bool = False, **__) -> Union[float, None]:
        """get_current_slider_value_by_identifier(sim_info, custom_slider, use_persisted_value=True)

        Retrieve the current value of a slider.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param custom_slider: The slider to check.
        :type custom_slider: CSFSlider
        :param use_persisted_value: If True, the persisted value will be used rather than the current value on the Sim. If False, the current value on the Sim will be used. Default is True.
        :type use_persisted_value: bool, optional
        :return: The current slider value for the slider or None if the slider does not exist.
        :rtype: Union[float, None]
        """
        if sim_info is None or custom_slider is None:
            return None
        sim_data = None
        current_sim_type = None
        applied_sliders = None
        return_value = None
        if use_persisted_value:
            sim_data = CSFSimSliderSystemData(sim_info)
            current_sim_type = CommonSimTypeUtils.determine_sim_type(sim_info, use_current_occult_type=True)
            applied_sliders = sim_data.applied_sliders
            slider_value = applied_sliders.get_slider_value(current_sim_type, custom_slider.raw_display_name)
            if slider_value is not None:
                return slider_value

        try:
            facial_attributes = self._get_facial_attributes(sim_info)

            # noinspection PyUnresolvedReferences
            for body_modifier in facial_attributes.body_modifiers:
                if body_modifier.amount == 0.0:
                    continue
                if custom_slider.has_negative_modifier_id() and body_modifier.key == custom_slider.negative_modifier_id:
                    self.log.debug(f'Found existing negative body modifier value {body_modifier.amount} with key {body_modifier.key}')
                    if not custom_slider.is_body_modifier:
                        self.log.format_error_with_message(f'Not a BODY MODIFIER {custom_slider.raw_display_name}', custom_slider=custom_slider.raw_display_name, throw=False)
                    return_value = (body_modifier.amount * -1.0)/0.01
                    break
                if custom_slider.has_positive_modifier_id() and body_modifier.key == custom_slider.positive_modifier_id:
                    self.log.debug(f'Found existing positive body modifier value {body_modifier.amount} with key {body_modifier.key}')
                    if not custom_slider.is_body_modifier:
                        self.log.format_error_with_message(f'Not a BODY MODIFIER {custom_slider.raw_display_name}', custom_slider=custom_slider.raw_display_name, throw=False)
                    return_value = body_modifier.amount/0.01
                    break

            if return_value is not None:
                return return_value

            # noinspection PyUnresolvedReferences
            for aged_body_modifier in facial_attributes.aged_body_modifiers:
                if aged_body_modifier.amount == 0.0:
                    continue
                if custom_slider.has_negative_modifier_id() and aged_body_modifier.key == custom_slider.negative_modifier_id:
                    self.log.debug(f'Found existing negative aged body modifier value {aged_body_modifier.amount} with key {aged_body_modifier.key}')
                    if not custom_slider.is_body_modifier:
                        self.log.format_error_with_message(f'Not an AGED BODY MODIFIER {custom_slider.raw_display_name}', custom_slider=custom_slider.raw_display_name, throw=False)
                    return_value = (aged_body_modifier.amount * -1.0)/0.01
                    break
                if custom_slider.has_positive_modifier_id() and aged_body_modifier.key == custom_slider.positive_modifier_id:
                    self.log.debug(f'Found existing positive aged body modifier value {aged_body_modifier.amount} with key {aged_body_modifier.key}')
                    if not custom_slider.is_body_modifier:
                        self.log.format_error_with_message(f'Not an AGED BODY MODIFIER {custom_slider.raw_display_name}', custom_slider=custom_slider.raw_display_name, throw=False)
                    return_value = aged_body_modifier.amount/0.01
                    break

            if return_value is not None:
                return return_value

            # noinspection PyUnresolvedReferences
            for face_modifier in facial_attributes.face_modifiers:
                if face_modifier.amount == 0.0:
                    continue
                if custom_slider.has_negative_modifier_id() and face_modifier.key == custom_slider.negative_modifier_id:
                    self.log.debug(f'Found existing negative face modifier value {face_modifier.amount} with key {face_modifier.key}')
                    if not custom_slider.is_face_modifier:
                        self.log.format_error_with_message(f'Not a FACE MODIFIER {custom_slider.raw_display_name}', custom_slider=custom_slider.raw_display_name, throw=False)
                    return_value = (face_modifier.amount * -1.0)/0.01
                    break
                if custom_slider.has_positive_modifier_id() and face_modifier.key == custom_slider.positive_modifier_id:
                    self.log.debug(f'Found existing positive face modifier value {face_modifier.amount} with key {face_modifier.key}')
                    if not custom_slider.is_face_modifier:
                        self.log.format_error_with_message(f'Not a FACE MODIFIER {custom_slider.raw_display_name}', custom_slider=custom_slider.raw_display_name, throw=False)
                    return_value = face_modifier.amount/0.01
                    break

            if return_value is not None:
                return return_value

            # noinspection PyUnresolvedReferences
            for aged_face_modifier in facial_attributes.aged_face_modifiers:
                if aged_face_modifier.amount == 0.0:
                    continue
                if custom_slider.has_negative_modifier_id() and aged_face_modifier.key == custom_slider.negative_modifier_id:
                    self.log.debug(f'Found existing negative aged face modifier value {aged_face_modifier.amount} with key {aged_face_modifier.key}')
                    if not custom_slider.is_face_modifier:
                        self.log.format_error_with_message(f'Not an AGED FACE MODIFIER {custom_slider.raw_display_name}', custom_slider=custom_slider.raw_display_name, throw=False)
                    return_value = (aged_face_modifier.amount * -1.0)/0.01
                    break
                if custom_slider.has_positive_modifier_id() and aged_face_modifier.key == custom_slider.positive_modifier_id:
                    self.log.debug(f'Found existing positive aged face modifier value {aged_face_modifier.amount} with key {aged_face_modifier.key}')
                    if not custom_slider.is_face_modifier:
                        self.log.format_error_with_message(f'Not an AGED FACE MODIFIER {custom_slider.raw_display_name}', custom_slider=custom_slider.raw_display_name, throw=False)
                    return_value = aged_face_modifier.amount/0.01
                    break

            if return_value is not None:
                return return_value

            self.log.format_with_message(f'Modifier not found. {custom_slider.raw_display_name}')
            return_value = 0.0
            return return_value
        finally:
            if use_persisted_value and applied_sliders is not None and sim_data is not None and current_sim_type is not None:
                if return_value is not None:
                    applied_sliders.set_slider_value(current_sim_type, custom_slider.raw_display_name, return_value)
                    sim_data.applied_sliders = applied_sliders

    def remove_slider(self, sim_info: SimInfo, custom_slider: CSFSlider, trigger_event: bool = True, persist_value: bool = False, **__) -> bool:
        """ Remove a slider from a Sim. """
        try:
            if sim_info is None or custom_slider is None:
                self.log.debug('Missing sim_info or custom_slider')
                return False

            current_slider_amount = self.get_current_slider_value(sim_info, custom_slider, use_persisted_value=True)

            if persist_value:
                sim_data = CSFSimSliderSystemData(sim_info)
                current_sim_type = CommonSimTypeUtils.determine_sim_type(sim_info, use_current_occult_type=True)
                applied_sliders = sim_data.applied_sliders
                slider_amount = applied_sliders.get_slider_value(current_sim_type, custom_slider.raw_display_name)
                if slider_amount is not None:
                    current_slider_amount = slider_amount
                applied_sliders.clear_slider_value(current_sim_type, custom_slider.raw_display_name)
                sim_data.applied_sliders = applied_sliders

            self.log.debug('Applying facial attribute.')
            modified_facial_attributes = self._get_existing_modifiers_for_edit(sim_info, exclude_modifier_ids=(*custom_slider.get_modifier_ids(), custom_slider.positive_modifier_id, custom_slider.negative_modifier_id))

            self._set_facial_attributes(sim_info, modified_facial_attributes)
            if trigger_event:
                from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
                CommonEventRegistry().dispatch(CSFSliderValueChanged(sim_info, custom_slider, current_slider_amount, 0.0))
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, f'Error occurred while applying slider: \'{custom_slider.raw_display_name}\'', exception=ex)

    def remove_slider_by_name(self, sim_info: SimInfo, name: str, trigger_event: bool = True, persist_value: bool = False, **__) -> bool:
        """ Remove a slider with its name. """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        self.log.debug(f'Attempting to remove slider with name {name}')
        custom_sliders = CSFSliderQueryUtils().get_sliders_by_name(sim_info, name)
        if not custom_sliders:
            self.log.debug(f'No sliders found with name: {name}')
            return False
        custom_slider = next(iter(custom_sliders))
        if custom_slider is None:
            self.log.debug(f'No slider found with name: {name}')
            return False
        self.log.debug(f'Slider found with name {name}, attempting to remove.')
        return self.remove_slider(sim_info, custom_slider, trigger_event=trigger_event, persist_value=persist_value)

    def apply_slider(self, sim_info: SimInfo, custom_slider: CSFSlider, amount: float, trigger_event: bool = True, persist_value: bool = False, **__) -> bool:
        """ Apply a slider to a Sim. """
        try:
            if sim_info is None or custom_slider is None:
                self.log.debug('Missing sim_info or custom_slider')
                return False

            if not custom_slider.is_available_for(sim_info):
                self.log.format_with_message('The specified slider is not available for the Sim.', sim=sim_info, slider=custom_slider)
                return False

            amount = self._clamp_value(amount, custom_slider)

            if amount == 0.0:
                self.log.format_with_message('Value is Zero, so we will remove the value instead.', slider_name=custom_slider.raw_display_name)
                return self.remove_slider(sim_info, custom_slider, trigger_event=trigger_event, persist_value=persist_value)

            self.log.debug(f'Determining which slider to use for {custom_slider.raw_display_name} with amount {amount}.')
            if amount > 0:
                self.log.debug(f'Amount is greater than 0.0. It is {amount}.')
                if not custom_slider.has_positive_modifier_id():
                    self.log.debug('No positive modifier id.')
                    return False
                self.log.debug('Has positive modifier id.')
                slider_amount = amount * 0.01
                slider_id = custom_slider.positive_modifier_id
            else:
                self.log.debug(f'Amount is less than zero. It is {amount}.')
                if not custom_slider.has_negative_modifier_id():
                    self.log.debug('No negative modifier id.')
                    return False
                self.log.debug('Has negative modifier id.')
                slider_amount = amount * -0.01
                slider_id = custom_slider.negative_modifier_id

            if slider_id == 0:
                self.log.error('Slider key is zero!')
                return False

            current_slider_amount = self.get_current_slider_value(sim_info, custom_slider, use_persisted_value=True)

            if persist_value:
                sim_data = CSFSimSliderSystemData(sim_info)

                current_sim_type = CommonSimTypeUtils.determine_sim_type(sim_info, use_current_occult_type=True)
                applied_sliders = sim_data.applied_sliders
                current_slider_amount = applied_sliders.get_slider_value(current_sim_type, custom_slider.raw_display_name)
                applied_sliders.set_slider_value(current_sim_type, custom_slider.raw_display_name, amount)
                sim_data.applied_sliders = applied_sliders

            self.log.format_with_message(f'Applying facial attribute, current: {current_slider_amount}.')
            modified_facial_attributes = self._get_existing_modifiers_for_edit(sim_info, exclude_modifier_ids=(*custom_slider.get_modifier_ids(), custom_slider.positive_modifier_id, custom_slider.negative_modifier_id))

            self.log.debug('Adding the custom slider because the amount is greater than zero.')
            new_modifier = BlobSimFacialCustomizationData().Modifier()
            new_modifier.key = slider_id
            new_modifier.amount = self._clamp_value(slider_amount, custom_slider)
            if custom_slider.is_face_modifier:
                # noinspection PyUnresolvedReferences
                modified_facial_attributes.face_modifiers.append(new_modifier)
                # noinspection PyUnresolvedReferences
                modified_facial_attributes.aged_face_modifiers.append(new_modifier)
            elif custom_slider.is_body_modifier:
                # noinspection PyUnresolvedReferences
                modified_facial_attributes.body_modifiers.append(new_modifier)
                # noinspection PyUnresolvedReferences
                modified_facial_attributes.aged_body_modifiers.append(new_modifier)

            self._set_facial_attributes(sim_info, modified_facial_attributes)
            if trigger_event:
                self.log.format_with_message(f'Triggering event with amount {amount}.')
                from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
                CommonEventRegistry().dispatch(CSFSliderValueChanged(sim_info, custom_slider, current_slider_amount, amount))
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, f'Error occurred while applying slider: \'{custom_slider.raw_display_name}\'', exception=ex)

    def apply_slider_by_name(self, sim_info: SimInfo, name: str, amount: float, trigger_event: bool = True, persist_value: bool = False, **__) -> bool:
        """ Apply a slider with its name. """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        self.log.debug(f'Attempting to apply slider with name {name} and amount {amount}')
        custom_sliders = CSFSliderQueryUtils().get_sliders_by_name(sim_info, name)
        if not custom_sliders:
            self.log.debug(f'No sliders found with name: {name}')
            return False
        custom_slider = next(iter(custom_sliders))
        if custom_slider is None:
            self.log.debug(f'No slider found with name: {name}')
            return False
        self.log.debug('Slider found, attempting to apply.')
        return self.apply_slider(sim_info, custom_slider, amount, trigger_event=trigger_event, persist_value=persist_value)

    def apply_slider_by_identifier(self, sim_info: SimInfo, identifier: str, amount: float, trigger_event: bool = True, persist_value: bool = False, **__) -> bool:
        """ Apply a slider with its identifier. """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        self.log.debug(f'Attempting to apply slider with identifier {identifier} and amount {amount}')
        custom_slider = CSFSliderQueryUtils().locate_by_identifier(identifier)
        if custom_slider is None:
            self.log.debug(f'No slider found with identifier: {identifier}')
            return False
        self.log.debug('Slider found, attempting to apply.')
        return self.apply_slider(sim_info, custom_slider, amount, trigger_event=trigger_event, persist_value=persist_value)

    def apply_random(self, sim_info: SimInfo, custom_slider: CSFSlider, trigger_event: bool = True, persist_value: bool = False, **__) -> bool:
        """ Apply a random value for a slider. """
        name = custom_slider.raw_display_name
        amount = random.randint(int(custom_slider.minimum_value), int(custom_slider.maximum_value))
        self.log.debug(f'Attempting to apply slider with name {name} and amount {amount}')
        return self.apply_slider(sim_info, custom_slider, amount, trigger_event=trigger_event, persist_value=persist_value)

    def reset_slider(self, sim_info: SimInfo, custom_slider: CSFSlider, trigger_event: bool = True, persist_value: bool = False, **__) -> bool:
        """ Reset a Slider to its default for a Sim. """
        return self.apply_slider(sim_info, custom_slider, 0.0, trigger_event=trigger_event, persist_value=persist_value)

    def reset_all_sliders(self, sim_info: SimInfo, trigger_event: bool = True, persist_value: bool = False, **__) -> bool:
        """ Reset all Custom Sliders for a Sim. """
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        for custom_slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            self.reset_slider(sim_info, custom_slider, trigger_event=trigger_event, persist_value=persist_value)
        return True

    def _clamp_value(self, value: float, custom_slider: CSFSlider) -> float:
        return min(max(value, custom_slider.minimum_value), custom_slider.maximum_value)
