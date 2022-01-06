"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple, List

from cncustomsliderframework.custom_slider_application_service import CSFCustomSliderApplicationService
from cncustomsliderframework.dialogs.slider_template_dialog import CSFSliderTemplateDialog
from cncustomsliderframework.dtos.sliders.slider import CSFSlider
from cncustomsliderframework.enums.string_ids import CSFStringId
from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.enums.slider_category import CSFSliderCategory
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_option_category import \
    CommonDialogObjectOptionCategory
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.enums.icons_enum import CommonIconId
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class CSFCustomizeSlidersDialog(HasLog):
    """ A dialog for changing custom sliders. """
    def __init__(self, on_close: Callable[[], None]=CommonFunctionUtils.noop):
        from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
        super().__init__()
        self._on_close = on_close
        self.slider_application_service = CSFCustomSliderApplicationService()
        self._slider_query_utils = CSFSliderQueryUtils()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'csf_customize_sliders_dialog'

    def open(self, sim_info: SimInfo, page: int=1) -> None:
        """ Open the dialog. """
        self.log.format_with_message('Opening customize sliders dialog for Sim.', sim=sim_info)

        def _on_close() -> None:
            self.log.debug('Customize Slider dialog closed.')
            if self._on_close is not None:
                self._on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            CSFStringId.CUSTOMIZE_SLIDERS,
            CSFStringId.CHOOSE_SLIDERS_TO_MODIFY,
            mod_identity=self.mod_identity,
            on_close=_on_close,
            per_page=400
        )

        def _reopen() -> None:
            self.log.debug('Reopening customize sliders dialog.')
            self.open(sim_info, page=option_dialog.current_page)

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CSFStringId.SLIDER_TEMPLATES_NAME,
                    CSFStringId.SLIDER_TEMPLATES_DESCRIPTION,
                    tag_list=[slider_category.name for slider_category in CSFSliderCategory.values]
                ),
                on_chosen=lambda *_, **__: CSFSliderTemplateDialog(on_close=_reopen).open(sim_info),
                always_visible=True
            )
        )

        def _on_reset_all_sliders() -> None:
            self.log.debug('Confirming all sliders reset.')

            def _on_confirm(_) -> None:
                self.log.debug('Resetting all sliders.')
                self.slider_application_service.reset_all_sliders(sim_info)
                _reopen()

            def _on_cancel(_) -> None:
                self.log.debug('Cancelled resetting of all sliders.')
                _reopen()

            CommonOkCancelDialog(
                CSFStringId.CONFIRMATION,
                CSFStringId.ARE_YOU_SURE_YOU_WANT_TO_RESET_ALL_SLIDERS,
                mod_identity=self.mod_identity
            ).show(on_ok_selected=_on_confirm, on_cancel_selected=_on_cancel)

        self.log.debug('Opening Customize Slider dialog.')

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CSFStringId.RESET_ALL_SLIDERS_NAME,
                    CSFStringId.RESET_ALL_SLIDERS_DESCRIPTION,
                    tag_list=[slider_category.name for slider_category in CSFSliderCategory.values]
                ),
                on_chosen=lambda *_, **__: _on_reset_all_sliders(),
                always_visible=True
            )
        )

        sliders: Tuple[CSFSlider] = self._slider_query_utils.get_sliders_for_sim(sim_info)

        if not sliders:
            from cncustomsliderframework.sliders.slider_query_registry import CSFSliderQueryRegistry
            if CSFSliderQueryRegistry()._collecting:
                CommonOkDialog(
                    CSFStringId.SLIDERS_ARE_STILL_LOADING,
                    CSFStringId.SLIDERS_ARE_STILL_LOADING_DESCRIPTION,
                    description_tokens=(CSFStringId.FINISHED_LOADING_SLIDERS,),
                    mod_identity=ModInfo.get_identity()
                ).show()
            else:
                CommonOkDialog(
                    CSFStringId.NO_SLIDERS_FOUND,
                    CSFStringId.NO_SLIDERS_FOUND,
                    mod_identity=ModInfo.get_identity()
                ).show()
            _on_close()
            return

        self.log.debug('Adding slider count {}'.format(len(sliders)))
        sorted_sliders = sorted(sliders, key=lambda s: s.name)
        slider_categories: List[CSFSliderCategory] = list()
        object_categories: List[str] = list()
        for custom_slider in sorted_sliders:
            for slider_category in custom_slider.categories:
                if slider_category.name in object_categories:
                    continue
                slider_categories.append(slider_category)
                object_categories.append(slider_category.name)

        def _on_randomize_slider_category(category_name: str, category: CSFSliderCategory):
            self.log.debug('Confirming reset of sliders in category {}.'.format(category_name))

            def _on_confirm(_) -> None:
                self.log.debug('Randomizing all sliders in category {}.'.format(category_name))
                for slider in sorted_sliders:
                    if category not in slider.categories:
                        continue
                    self.slider_application_service.apply_random(sim_info, slider)
                _reopen()

            def _on_cancel(_) -> None:
                self.log.debug('Cancelled randomization of sliders in category {}.'.format(category_name))
                _reopen()

            CommonOkCancelDialog(
                CSFStringId.CONFIRMATION,
                CSFStringId.RANDOMIZE_SLIDER_CONFIRMATION,
                mod_identity=self.mod_identity
            ).show(on_ok_selected=_on_confirm, on_cancel_selected=_on_cancel)

        for slider_category in slider_categories:
            option_dialog.add_option(
                CommonDialogSelectOption(
                    slider_category.name,
                    slider_category,
                    CommonDialogOptionContext(
                        CSFStringId.RANDOMIZE_SLIDER_NAME,
                        CSFStringId.RANDOMIZE_SLIDER_DESCRIPTION,
                        title_tokens=(slider_category.name, ),
                        description_tokens=(slider_category.name, ),
                        tag_list=[slider_category.name for slider_category in CSFSliderCategory.values]
                    ),
                    on_chosen=_on_randomize_slider_category,
                    always_visible=True
                )
            )

        def _on_slider_changed(slider_unique_identifier: str, _custom_slider: CSFSlider):
            if slider_unique_identifier is None or _custom_slider is None:
                self.log.debug('No slider chosen, dialog closed.')
                _reopen()
                return
            self._change_or_remove_slider_option(sim_info, _custom_slider, on_close=_reopen)

        for custom_slider in sorted_sliders:
            if custom_slider.description is not None:
                # noinspection PyTypeChecker
                option_description = CommonLocalizationUtils.create_localized_string(custom_slider.description, tokens=(str(0.0), str(custom_slider.minimum_value), str(custom_slider.maximum_value)))
            else:
                # noinspection PyTypeChecker
                option_description = CommonLocalizationUtils.create_localized_string(CSFStringId.CHANGE_THE_SLIDER, tokens=(custom_slider.display_name, ))

            option_dialog.add_option(
                CommonDialogSelectOption(
                    custom_slider.unique_identifier,
                    custom_slider,
                    CommonDialogOptionContext(
                        custom_slider.display_name,
                        option_description,
                        title_tokens=(str(self.slider_application_service.get_current_slider_value(sim_info, custom_slider)),),
                        icon=CommonResourceUtils.get_resource_key(Types.PNG, custom_slider.icon_id) if custom_slider.icon_id else None,
                        tag_list=tuple([category.name for category in custom_slider.categories])
                    ),
                    on_chosen=_on_slider_changed
                )
            )

        categories: List[CommonDialogObjectOptionCategory] = list()

        for category in object_categories:
            # noinspection PyTypeChecker
            categories.append(
                CommonDialogObjectOptionCategory(
                    category,
                    icon=CommonIconId.S4CLIB_UNFILLED_CIRCLE_ICON
                )
            )

        self.log.debug('Showing slider options.')

        option_dialog.show(
            sim_info=sim_info,
            page=page,
            categories=categories
        )

    def _change_or_remove_slider_option(
        self,
        sim_info: SimInfo,
        custom_slider: CSFSlider,
        on_close: Callable[[], None]
    ):
        def _reopen() -> None:
            self._change_or_remove_slider_option(sim_info, custom_slider, on_close)

        def _on_slider_changed(slider_unique_identifier: str, amount: float, outcome: CommonChoiceOutcome):
            if slider_unique_identifier is None or amount is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                self.log.debug('No slider chosen, dialog closed, or no amount specified.')
                _reopen()
                return
            self.log.debug('Slider changed, attempting to apply.')
            self.slider_application_service.apply_slider(sim_info, custom_slider, amount, trigger_event=True)
            _reopen()

        def _on_remove_slider() -> None:
            self.slider_application_service.remove_slider(sim_info, custom_slider, trigger_event=True)
            _reopen()

        if custom_slider.description is not None:
            # noinspection PyTypeChecker
            option_description = CommonLocalizationUtils.create_localized_string(custom_slider.description, tokens=(str(0.0), str(custom_slider.minimum_value), str(custom_slider.maximum_value)))
        else:
            # noinspection PyTypeChecker
            option_description = CommonLocalizationUtils.create_localized_string(CSFStringId.CHANGE_THE_SLIDER, tokens=(custom_slider.display_name, ))

        option_dialog = CommonChooseObjectOptionDialog(
            custom_slider.display_name,
            option_description,
            mod_identity=self.mod_identity,
            on_close=on_close,
            per_page=400
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CSFStringId.RESET_SLIDER_NAME,
                    CSFStringId.RESET_SLIDER_DESCRIPTION
                ),
                on_chosen=lambda *_, **__: _on_remove_slider(),
                always_visible=True
            )
        )

        option_dialog.add_option(
            CommonDialogInputFloatOption(
                custom_slider.unique_identifier,
                self.slider_application_service.get_current_slider_value(sim_info, custom_slider),
                CommonDialogOptionContext(
                    CSFStringId.CHANGE_SLIDER_VALUE_NAME,
                    CSFStringId.CHANGE_SLIDER_VALUE_DESCRIPTION,
                    title_tokens=(str(self.slider_application_service.get_current_slider_value(sim_info, custom_slider)),),
                    icon=custom_slider.icon_id or None
                ),
                min_value=custom_slider.minimum_value,
                max_value=custom_slider.maximum_value,
                on_chosen=_on_slider_changed,
                dialog_description_identifier=CSFStringId.DEFAULT_MIN_MAX,
                dialog_description_tokens=(option_description, str(0.0), str(custom_slider.minimum_value), str(custom_slider.maximum_value))
            )
        )

        option_dialog.show(sim_info=sim_info)
