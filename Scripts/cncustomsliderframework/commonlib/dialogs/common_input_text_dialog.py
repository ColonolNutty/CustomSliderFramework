"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import Any, Callable, Union, Iterator, Dict

from pprint import pformat
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs._common_ui_dialog_text_input_ok_cancel import _CommonUiDialogTextInputOkCancel
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_generic import UiDialogTextInput
from sims4communitylib.modinfo import ModInfo


class CommonInputTextDialog(CommonDialog):
    """CommonInputTextDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        initial_value,\
        title_tokens=(),\
        description_tokens=(),\
        substitute_characters=()\
    )

    Create a dialog that prompts the player to enter text.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_input_text_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_input_text_dialog():

            def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
                pass

            # LocalizedStrings within other LocalizedStrings
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
            from sims4communitylib.utils.common_icon_utils import CommonIconUtils
            dialog = CommonInputTextDialog(
                ModInfo.get_identity(),
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                'test text',
                title_tokens=title_tokens,
                description_tokens=description_tokens
            )
            dialog.show(on_submit=_on_chosen)

    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity
    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param initial_value: The initial text that will appear in the input box.
    :type initial_value: str
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param substitute_characters: A mapping of characters with their replacements if found within the entered text. Default is None.
    :type substitute_characters: Dict[str, str], optional
    """
    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        initial_value: str,
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        substitute_characters: Dict[str, str]=None
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity
        )
        self.initial_value = initial_value
        self.substitute_characters = substitute_characters

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_input_text_dialog'

    def show(
        self,
        on_submit: Callable[[Union[str, None], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop
    ):
        """show(\
            on_submit=CommonFunctionUtils.noop\
        )

        Show the dialog and invoke the callbacks upon the player submitting a value.

        :param on_submit: A callback invoked upon the player submitting a value. Default is CommonFunctionUtils.noop.
        :type on_submit: Callable[[Union[str, None], CommonChoiceOutcome], Any], optional
        """
        try:
            return self._show(
                on_submit=on_submit
            )
        except Exception as ex:
            self.log.error('show', exception=ex)

    def _show(
        self,
        on_submit: Callable[[Union[str, None], CommonChoiceOutcome], bool]=CommonFunctionUtils.noop
    ):
        self.log.debug('Attempting to display input text dialog.')

        if on_submit is None:
            raise ValueError('\'on_submit\' was None.')

        _dialog = self._create_dialog()
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        # noinspection PyBroadException
        def _on_submit(dialog: UiDialogTextInput) -> bool:
            try:
                input_text = CommonDialogUtils.get_input_value(dialog)
                if not input_text or not dialog.accepted:
                    self.log.debug('Dialog cancelled.')
                    return on_submit(None, CommonChoiceOutcome.CANCEL)
                self.log.format_with_message('Value entered, attempting to parse it.', value=input_text)

                input_text = str(input_text)

                if self.substitute_characters is not None:
                    for (char, replacement) in self.substitute_characters.items():
                        input_text = input_text.replace(char, replacement)

                self.log.format_with_message('Value entered.', input_value=input_text)
                result = on_submit(input_text, CommonChoiceOutcome.CHOICE_MADE)
                self.log.format_with_message('Finished handling input.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on submitting a value.', exception=ex)
            return False

        _dialog.add_listener(_on_submit)
        if self.initial_value is not None:
            _dialog.show_dialog(additional_tokens=(self.initial_value,))
        else:
            _dialog.show_dialog()

    def _create_dialog(self) -> Union[_CommonUiDialogTextInputOkCancel, None]:
        try:
            return _CommonUiDialogTextInputOkCancel.TunableFactory().default(
                CommonSimUtils.get_active_sim_info(),
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title
            )
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@sims4.commands.Command('s4clib_testing.show_input_text_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_input_text_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test input text dialog.')

    def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(pformat(choice), pformat(outcome)))

    try:
        # LocalizedStrings within other LocalizedStrings
        title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
        from sims4communitylib.utils.common_icon_utils import CommonIconUtils
        dialog = CommonInputTextDialog(
            ModInfo.get_identity(),
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            'test text',
            title_tokens=title_tokens,
            description_tokens=description_tokens
        )
        dialog.show(on_submit=_on_chosen)
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to show dialog', exception=ex)
        output('Failed to show dialog, please locate your exception log file.')
    output('Done showing.')
