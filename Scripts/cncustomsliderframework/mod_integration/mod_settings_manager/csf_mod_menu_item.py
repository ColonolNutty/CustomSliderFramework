"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
try:
    from cncustomsliderframework.custom_slider_registry import CSFCustomSliderRegistry
    from cncustomsliderframework.dialogs.customize_sliders_dialog import CSFCustomizeSlidersDialog
    from cncustomsliderframework.interactions.customize_sliders import CSFCustomizeSlidersInteraction
    from cncustomsliderframework.modinfo import ModInfo
    from typing import Callable, Any, Union
    from sims.sim_info import SimInfo
    from sims4communitylib.mod_support.mod_identity import CommonModIdentity
    from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
    from sims4communitylib.utils.common_type_utils import CommonTypeUtils
    from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
    from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
    from sims4modsettingsmenu.registration.mod_settings_menu_item import S4MSMMenuItem
    from sims4modsettingsmenu.registration.mod_settings_registry import S4MSMModSettingsRegistry
    from event_testing.results import TestResult
    from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
    from sims4communitylib.utils.common_log_registry import CommonLogRegistry
    from cncustomsliderframework.enums.string_ids import CSFStringId
    from protocolbuffers.Localization_pb2 import LocalizedString


    class _CSFMSMMenuItem(S4MSMMenuItem):
        # noinspection PyMissingOrEmptyDocstring
        @property
        def mod_identity(self) -> CommonModIdentity:
            return ModInfo.get_identity()

        # noinspection PyMissingOrEmptyDocstring
        @property
        def title(self) -> Union[int, str, LocalizedString, None]:
            return CSFStringId.CUSTOMIZE_SLIDERS

        # noinspection PyMissingOrEmptyDocstring
        @property
        def log_identifier(self) -> str:
            return 'csf_msm_menu_item'

        # noinspection PyMissingOrEmptyDocstring
        def is_available_for(self, source_sim_info: SimInfo, target: Any=None) -> bool:
            self.log.debug('Checking if customize sliders are available for \'{}\' and Target \'{}\'.'.format(CommonSimNameUtils.get_full_name(source_sim_info), target))
            if target is None or not CommonTypeUtils.is_sim_or_sim_info(target):
                self.log.debug('Target is not a Sim.')
                return False
            target_sim_info = CommonSimUtils.get_sim_info(target)
            if not CSFCustomSliderRegistry().has_available_sliders(target_sim_info):
                self.log.debug('Failed, No sliders available for the Target Sim.')
                return False
            self.log.debug('Menu is available for Source Sim and Target Sim.')
            return True

        # noinspection PyMissingOrEmptyDocstring
        def show(
            self,
            source_sim_info: SimInfo,
            *args,
            target: Any=None,
            on_close: Callable[..., Any]=CommonFunctionUtils.noop,
            **kwargs
        ):
            self.log.debug('Showing CSF Settings.')
            target_sim_info = CommonSimUtils.get_sim_info(target)
            CSFCustomizeSlidersDialog(on_close=on_close).open(target_sim_info)


    S4MSMModSettingsRegistry().register_menu_item(_CSFMSMMenuItem())

    log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'csf_customize_sliders')

    # noinspection PyUnusedLocal
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CSFCustomizeSlidersInteraction, CSFCustomizeSlidersInteraction.on_test.__name__)
    def _hide_interaction(original, cls, *_, **__) -> TestResult:
        log.debug('Hiding the Customize Sliders interaction in favor of the Mod Settings Menu.')
        return TestResult.NONE
except:
    pass
