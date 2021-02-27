"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from cncustomsliderframework.commonlib.dialogs.option_dialogs.options.objects.common_dialog_input_text_option import \
    CommonDialogInputTextOption
from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.enums.string_ids import CSFStringId
from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.slider_templates.slider_template import CSFSliderTemplate
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import \
    CommonDialogObjectOption
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class CSFSliderTemplateDialog(HasLog):
    """ A dialog for loading, saving, and applying slider templates. """
    _SELECTED_TEMPLATE: CSFSliderTemplate = None
    
    def __init__(self, on_close: Callable[[], None]=CommonFunctionUtils.noop):
        super().__init__()
        self._on_close = on_close
        from cncustomsliderframework.slider_templates.slider_template_utils import CSFSliderTemplateUtils
        self._template_utils = CSFSliderTemplateUtils()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_slider_template_dialog'

    def open(self, sim_info: SimInfo, page: int=1) -> None:
        """ Open the dialog. """
        self.log.format_with_message('Opening dialog.', sim=sim_info)

        def _on_close() -> None:
            self.log.debug('Slider Template dialog closed.')
            if self._on_close is not None:
                self._on_close()

        def _reopen() -> None:
            self.log.debug('Reopening slider template dialog.')
            self.open(sim_info, page=option_dialog.current_page)

        option_dialog = CommonChooseObjectOptionDialog(
            CSFStringId.SLIDER_TEMPLATES_NAME,
            CSFStringId.SLIDER_TEMPLATES_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close,
            per_page=400
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CSFStringId.SELECTED_TEMPLATE,
                    0,
                    title_tokens=(CSFSliderTemplateDialog._SELECTED_TEMPLATE.template_name if CSFSliderTemplateDialog._SELECTED_TEMPLATE is not None else CSFStringId.NO_TEMPLATE_SELECTED,)
                ),
                on_chosen=lambda *_, **__: self._select_template(sim_info, on_close=_reopen)
            )
        )

        def _on_apply_template_to_sim() -> None:
            self.log.debug('Confirming all sliders reset.')
            if CSFSliderTemplateDialog._SELECTED_TEMPLATE is None:
                def _on_acknowledge(_) -> None:
                    _reopen()

                CommonOkDialog(
                    CSFStringId.NO_TEMPLATE_SELECTED,
                    CSFStringId.PLEASE_SELECT_A_TEMPLATE,
                    mod_identity=self.mod_identity
                ).show(on_acknowledged=_on_acknowledge)
                return

            def _on_confirm(_) -> None:
                self.log.debug('Applying template to Sim.')
                CSFSliderTemplateDialog._SELECTED_TEMPLATE.apply_to_sim(sim_info)
                _reopen()

            def _on_cancel(_) -> None:
                self.log.debug('Cancelled template apply.')
                _reopen()

            CommonOkCancelDialog(
                CSFStringId.CONFIRMATION,
                CSFStringId.APPLY_TEMPLATE_TO_SIM_CONFIRMATION_DESCRIPTION,
                description_tokens=(sim_info,),
                mod_identity=self.mod_identity
            ).show(on_ok_selected=_on_confirm, on_cancel_selected=_on_cancel)

        self.log.debug('Opening Customize Slider dialog.')

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CSFStringId.APPLY_TEMPLATE_TO_SIM_NAME,
                    CSFStringId.APPLY_TEMPLATE_TO_SIM_DESCRIPTION,
                    description_tokens=(sim_info,),
                    is_enabled=CSFSliderTemplateDialog._SELECTED_TEMPLATE is not None
                ),
                on_chosen=lambda *_, **__: _on_apply_template_to_sim()
            )
        )

        def _on_save_as_template(_: str, template_name: str, outcome: CommonChoiceOutcome):
            if _ is None or template_name is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                self.log.debug('No template name entered, dialog closed.')
                _reopen()
                return
            self.log.format_with_message('Template name entered.', template_name=template_name)
            if template_name in self._template_utils.template_library:
                def _on_yes(_) -> None:
                    self.log.debug('Saving template.')
                    self._template_utils.save_sliders_of(sim_info, template_name)
                    _reopen()

                def _on_no(_) -> None:
                    self.log.debug('Cancelled saving template.')
                    _reopen()

                CommonOkCancelDialog(
                    CSFStringId.TEMPLATE_ALREADY_EXISTS_NAME,
                    CSFStringId.TEMPLATE_ALREADY_EXISTS_DESCRIPTION,
                    description_tokens=(template_name,),
                    ok_text_identifier=CSFStringId.YES,
                    cancel_text_identifier=CSFStringId.NO,
                    mod_identity=self.mod_identity
                ).show(on_ok_selected=_on_yes, on_cancel_selected=_on_no)
                return

            self._template_utils.save_sliders_of(sim_info, template_name)
            _reopen()

        option_dialog.add_option(
            CommonDialogInputTextOption(
                self.mod_identity,
                'Save Template From Sim',
                CommonSimNameUtils.get_full_name(sim_info),
                CommonDialogOptionContext(
                    CSFStringId.CREATE_TEMPLATE_FROM_SIM_NAME,
                    CSFStringId.CREATE_TEMPLATE_FROM_SIM_DESCRIPTION,
                    title_tokens=(sim_info,),
                    description_tokens=(sim_info,)
                ),
                on_chosen=_on_save_as_template,
                dialog_description_identifier=CSFStringId.ENTER_A_NAME_FOR_YOUR_NEW_TEMPLATE
            )
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CSFStringId.VIEW_TEMPLATE_NAME,
                    CSFStringId.VIEW_TEMPLATE_DESCRIPTION,
                    is_enabled=CSFSliderTemplateDialog._SELECTED_TEMPLATE is not None,
                    title_tokens=(CSFSliderTemplateDialog._SELECTED_TEMPLATE.template_name if CSFSliderTemplateDialog._SELECTED_TEMPLATE is not None else CSFStringId.NO_TEMPLATE_SELECTED,)
                ),
                on_chosen=lambda *_, **__: self._view_template(sim_info, on_close=_reopen)
            )
        )

        option_dialog.show(
            sim_info=sim_info,
            page=page
        )

    def _select_template(self, sim_info: SimInfo, on_close: Callable[[], None]=None):
        self.log.format_with_message('Opening dialog.', sim=sim_info)

        def _on_close() -> None:
            self.log.debug('Slider Template dialog closed.')
            if on_close is not None:
                on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            CSFStringId.SELECTED_TEMPLATE,
            CSFStringId.PLEASE_SELECT_A_TEMPLATE,
            mod_identity=self.mod_identity,
            on_close=_on_close,
            per_page=400
        )

        self.log.debug('Opening Customize Slider dialog.')

        def _on_chosen(_: str, _chosen_template: CSFSliderTemplate):
            if _chosen_template is None:
                self.log.debug('No template name entered, dialog closed.')
                _on_close()
                return
            self.log.format_with_message('Template name entered.', template_name=_chosen_template.template_name)
            CSFSliderTemplateDialog._SELECTED_TEMPLATE = _chosen_template
            _on_close()

        for (template_name, template) in self._template_utils.template_library.items():
            template: CSFSliderTemplate = template
            option_dialog.add_option(
                CommonDialogObjectOption(
                    template_name,
                    template,
                    CommonDialogOptionContext(
                        template.display_name,
                        0,
                        icon=CommonIconUtils.load_filled_circle_icon() if CSFSliderTemplateDialog._SELECTED_TEMPLATE == template else CommonIconUtils.load_unfilled_circle_icon(),
                    ),
                    on_chosen=_on_chosen
                )
            )

        if not option_dialog.has_options():
            def _on_acknowledge(_) -> None:
                _on_close()

            CommonOkDialog(
                CSFStringId.NO_TEMPLATES_DETECTED_NAME,
                CSFStringId.NO_TEMPLATES_DETECTED_DESCRIPTION,
                mod_identity=self.mod_identity
            ).show(on_acknowledged=_on_acknowledge)
            return

        option_dialog.show(
            sim_info=sim_info
        )

    def _view_template(self, sim_info: SimInfo, on_close: Callable[[], None]=None):
        self.log.format_with_message('Opening view template dialog.', sim=sim_info)

        def _on_close() -> None:
            self.log.debug('Slider Template dialog closed.')
            if on_close is not None:
                on_close()

        def _reopen() -> None:
            self._view_template(sim_info, on_close=on_close)

        if CSFSliderTemplateDialog._SELECTED_TEMPLATE is None:
            def _on_acknowledge(_) -> None:
                _on_close()

            CommonOkDialog(
                CSFStringId.NO_TEMPLATE_SELECTED,
                CSFStringId.PLEASE_SELECT_A_TEMPLATE,
                mod_identity=self.mod_identity
            ).show(on_acknowledged=_on_acknowledge)
            return

        option_dialog = CommonChooseObjectOptionDialog(
            CSFStringId.VIEW_TEMPLATE_NAME,
            CSFStringId.VIEW_TEMPLATE_DESCRIPTION,
            mod_identity=self.mod_identity,
            on_close=_on_close,
            per_page=400
        )

        for (slider, amount) in CSFSliderTemplateDialog._SELECTED_TEMPLATE.get_sliders(sim_info):
            slider: CSFSlider = slider
            option_dialog.add_option(
                CommonDialogObjectOption(
                    slider.unique_identifier,
                    slider,
                    CommonDialogOptionContext(
                        0,
                        CSFStringId.STRING_PLUS_STRING,
                        description_tokens=(slider.display_name, str(amount),),
                        icon=CommonIconUtils.load_arrow_right_icon(),
                        is_enabled=False
                    ),
                    on_chosen=lambda *_, **__: _reopen()
                )
            )

        if not option_dialog.has_options():
            def _on_acknowledge(_) -> None:
                _on_close()

            CommonOkDialog(
                CSFStringId.NO_SLIDERS_DETECTED_NAME,
                CSFStringId.NO_SLIDERS_DETECTED_DESCRIPTION,
                mod_identity=self.mod_identity
            ).show(on_acknowledged=_on_acknowledge)
            return

        option_dialog.show(
            sim_info=sim_info
        )
