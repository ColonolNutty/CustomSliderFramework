"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Tuple

from cncustomsliderframework.custom_slider_application_service import CSFCustomSliderApplicationService
from cncustomsliderframework.custom_slider_registry import CSFCustomSliderRegistry
from cncustomsliderframework.dtos.custom_slider import CSFCustomSlider
from cncustomsliderframework.enums.string_ids import CSFStringId
from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.slider_category import CSFSliderCategory
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class CSFCustomizeSlidersDialog(CommonService, HasLog):
    """ A dialog for changing custom sliders. """
    def __init__(self) -> None:
        super().__init__()
        self.slider_application_service = CSFCustomSliderApplicationService()
        self.slider_registry = CSFCustomSliderRegistry()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_customize_sliders_dialog'

    def open(self, sim_info: SimInfo, on_close: Callable[..., Any]=None) -> None:
        """ Open the dialog. """
        self.log.debug('Opening customize sliders dialog for \'{}\'.'.format(CommonSimNameUtils.get_full_name(sim_info)))

        def _on_close() -> None:
            self.log.debug('Customize Slider dialog closed.')
            if on_close is not None:
                on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            CSFStringId.CUSTOMIZE_SLIDERS,
            CSFStringId.CHOOSE_SLIDERS_TO_MODIFY,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        def _reopen_dialog() -> None:
            self.log.debug('Reopening customize sliders dialog.')
            self.open(sim_info, on_close=on_close)

        def _on_reset_all_sliders() -> None:
            self.log.debug('Confirming all sliders reset.')

            def _on_confirm(_) -> None:
                self.log.debug('Resetting all sliders.')
                self.slider_application_service.reset_all_sliders(sim_info)
                _reopen_dialog()

            def _on_cancel(_) -> None:
                self.log.debug('Cancelled resetting of all sliders.')
                _reopen_dialog()

            CommonOkCancelDialog(
                CSFStringId.CONFIRMATION,
                CSFStringId.ARE_YOU_SURE_YOU_WANT_TO_RESET_ALL_SLIDERS,
                mod_identity=self.mod_identity
            ).show(on_ok_selected=_on_confirm, on_cancel_selected=_on_cancel)

        def _on_slider_changed(slider_name: str, amount: float, outcome: CommonChoiceOutcome):
            if slider_name is None or amount is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                self.log.debug('No slider chosen, dialog closed, or no amount specified.')
                _reopen_dialog()
                return
            self.log.debug('Slider changed, attempting to apply.')
            self.slider_application_service.apply_slider_by_name(sim_info, slider_name, amount)
            _reopen_dialog()

        self.log.debug('Opening Customize Slider dialog.')

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CSFStringId.RESET_ALL_SLIDERS_NAME,
                    CSFStringId.RESET_ALL_SLIDERS_DESCRIPTION,
                    tag_list=CSFSliderCategory.get_names()
                ),
                on_chosen=lambda *_, **__: _on_reset_all_sliders(),
                always_visible=True
            ),
        )

        sliders: Tuple[CSFCustomSlider] = CSFCustomSliderRegistry().get_loaded_sliders(sim_info)
        self.log.debug('Adding slider count {}'.format(len(sliders)))
        sorted_sliders = sorted(sliders, key=lambda s: s.raw_display_name)
        for custom_slider in sorted_sliders:
            if custom_slider.description is not None:
                option_description = custom_slider.description
            else:
                option_description = CSFStringId.CHANGE_THE_SLIDER

            option_dialog.add_option(
                CommonDialogInputFloatOption(
                    custom_slider.raw_display_name,
                    self.slider_application_service.get_current_facial_modifier_value(sim_info, custom_slider),
                    CommonDialogOptionContext(
                        custom_slider.display_name,
                        option_description,
                        description_tokens=(custom_slider.display_name, str(0.0), str(custom_slider.minimum_value), str(custom_slider.maximum_value)),
                        icon=custom_slider.icon_id or None,
                        tag_list=tuple([category.name for category in custom_slider.categories])
                    ),
                    min_value=custom_slider.minimum_value,
                    max_value=custom_slider.maximum_value,
                    on_chosen=_on_slider_changed,
                    dialog_description_identifier=CSFStringId.CHANGE_THE_SLIDER,
                    dialog_description_tokens=(custom_slider.display_name, str(0.0), str(custom_slider.minimum_value), str(custom_slider.maximum_value))
                )
            )

        self.log.debug('Showing slider options.')

        option_dialog.show(sim_info=sim_info)
