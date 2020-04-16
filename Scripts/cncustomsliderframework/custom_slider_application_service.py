"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cncustomsliderframework.dtos.custom_slider import CSFCustomSlider
from cncustomsliderframework.modinfo import ModInfo
from protocolbuffers import PersistenceBlobs_pb2
from sims.sim_info import SimInfo
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

    def get_current_slider_value(self, sim_info: SimInfo, custom_slider: CSFCustomSlider) -> float:
        """ Retrieve the value of an applied slider. """
        if sim_info is None or custom_slider is None:
            return False
        facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
        # noinspection PyPropertyAccess
        facial_attributes.MergeFromString(sim_info.facial_attributes)

        # noinspection PyUnresolvedReferences
        for face_modifier in facial_attributes.face_modifiers:
            if face_modifier.amount == 0.0:
                continue
            if custom_slider.has_positive_modifier_id() and face_modifier.key == custom_slider.positive_modifier_id:
                return face_modifier.amount/0.01
            if custom_slider.has_negative_modifier_id() and face_modifier.key == custom_slider.negative_modifier_id:
                return (face_modifier.amount * -1.0)/0.01
        return 0.0

    def apply_slider(self, sim_info: SimInfo, custom_slider: CSFCustomSlider, amount: float) -> bool:
        """ Apply a slider to a Sim. """
        if sim_info is None or custom_slider is None:
            return False
        facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
        # noinspection PyPropertyAccess
        facial_attributes.MergeFromString(sim_info.facial_attributes)
        modified_facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
        slider_to_add = PersistenceBlobs_pb2.BlobSimFacialCustomizationData().Modifier()
        slider_to_remove = PersistenceBlobs_pb2.BlobSimFacialCustomizationData().Modifier()

        if amount >= 0:
            self.log.debug('Amount is greater than or equal to 0.0. It is {}.'.format(amount))
            slider_to_add.amount = amount * 0.01
            if custom_slider.has_positive_modifier_id():
                self.log.debug('Has positive modifier id.')
                slider_to_add.key = custom_slider.positive_modifier_id
            if custom_slider.has_negative_modifier_id():
                self.log.debug('Has negative modifier id.')
                slider_to_remove.key = custom_slider.negative_modifier_id
        else:
            self.log.debug('Amount is less than zero. It is {}.'.format(amount))
            slider_to_add.amount = amount * -0.01
            if custom_slider.has_negative_modifier_id():
                self.log.debug('Has positive modifier id.')
                slider_to_add.key = custom_slider.negative_modifier_id
            if custom_slider.has_positive_modifier_id():
                self.log.debug('Has negative modifier id.')
                slider_to_remove.key = custom_slider.positive_modifier_id

        if slider_to_add.key == 0:
            self.log.error('Slider key is zero!')
            return False

        self.log.debug('Adding face modifiers.')
        # noinspection PyUnresolvedReferences
        for face_modifier in facial_attributes.face_modifiers:
            # Exclude the opposite modifier so it no longer applies.
            if face_modifier.key == slider_to_remove.key:
                self.log.debug('Skipping modifier with key {}'.format(slider_to_remove.key))
                continue
            # noinspection PyUnresolvedReferences
            modified_facial_attributes.face_modifiers.append(face_modifier)

        self.log.debug('Adding body modifiers.')
        # noinspection PyUnresolvedReferences
        for body_modifier in facial_attributes.body_modifiers:
            # noinspection PyUnresolvedReferences
            modified_facial_attributes.body_modifiers.append(body_modifier)

        self.log.debug('Adding sculpt modifiers.')
        # noinspection PyUnresolvedReferences
        for sculpt in facial_attributes.sculpts:
            # noinspection PyUnresolvedReferences
            modified_facial_attributes.sculpts.append(sculpt)

        self.log.debug('Applying slider.')
        # noinspection PyUnresolvedReferences
        modified_facial_attributes.face_modifiers.append(slider_to_add)
        sim_info.facial_attributes = modified_facial_attributes.SerializeToString()
        sim_info.resend_facial_attributes()

    def apply_slider_by_name(self, sim_info: SimInfo, name: str, amount: float) -> bool:
        """ Apply a slider with its name. """
        from cncustomsliderframework.custom_slider_registry import CSFCustomSliderRegistry
        custom_slider = CSFCustomSliderRegistry().find_custom_slider_by_name(sim_info, name)
        if custom_slider is None:
            return False
        return self.apply_slider(sim_info, custom_slider, amount)

    def reset_slider(self, sim_info: SimInfo, custom_slider: CSFCustomSlider) -> bool:
        """ Reset a Slider to its default for a Sim. """
        return self.apply_slider(sim_info, custom_slider, 0)

    def reset_all_sliders(self, sim_info: SimInfo) -> bool:
        """ Reset all Custom Sliders for a Sim. """
        from cncustomsliderframework.custom_slider_registry import CSFCustomSliderRegistry
        for custom_slider in CSFCustomSliderRegistry().get_loaded_sliders(sim_info):
            self.reset_slider(sim_info, custom_slider)
        return True
