"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cncustomsliderframework.custom_slider_application_service import CSFCustomSliderApplicationService
from cncustomsliderframework.modinfo import ModInfo
from protocolbuffers import PersistenceBlobs_pb2
from sims.sim_info import SimInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput


@CommonConsoleCommand(
    ModInfo.get_identity(),
    'csf.apply_slider',
    'Apply a new Slider value to a Sim by name.',
    command_arguments=(
        CommonConsoleCommandArgument('slider_name', 'Name of a Slider', 'The name of a slider.'),
        CommonConsoleCommandArgument('amount', 'Decimal Number', 'The new value to apply for the slider.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Name or ID', 'The Sim to modify.', is_optional=True, default_value='Active Sim'),
    ),
)
def _csf_apply_slider(output: CommonConsoleCommandOutput, slider_name: str, amount: float, sim_info: SimInfo = None):
    output(f'Applying slider \'{slider_name}\' with amount \'{amount}\'')
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    output(f'Applying slider to \'{sim_info}\'.')
    facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
    facial_attributes.MergeFromString(sim_info.facial_attributes)
    from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
    custom_sliders = CSFSliderQueryUtils().get_sliders_by_name(sim_info, slider_name)
    if not custom_sliders:
        output(f'Invalid Slider! \'{slider_name}\'')
        output('Available Sliders:')
        for custom_slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            output('>{}'.format(custom_slider.raw_display_name))
        return False
    custom_slider = next(iter(custom_sliders))
    if custom_slider is not None:
        output('Slider found.')
    else:
        output(f'Invalid Slider! \'{slider_name}\'')
        output('Available Sliders:')
        for custom_slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            output('>{}'.format(custom_slider.raw_display_name))
        return False
    # noinspection PyBroadException
    try:
        amount = float(amount)
    except:
        output(f'Amount must be a number! \'{amount}\'')
        return False
    output('Applying Sim Attributes!')
    return CSFCustomSliderApplicationService().apply_slider(sim_info, custom_slider, amount, trigger_event=True, persist_value=True)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    'csf.reset_slider',
    'Reset a slider by name for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('slider_name', 'Name of a Slider', 'The name of a slider.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Name or ID', 'The Sim to modify.', is_optional=True, default_value='Active Sim'),
    ),
)
def _csf_reset_slider(output: CommonConsoleCommandOutput, slider_name: str, sim_info: SimInfo = None):
    output(f'Resetting slider \'{slider_name}\'.')
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    output(f'Resetting slider for \'{sim_info}\'.')
    from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
    custom_sliders = CSFSliderQueryUtils().get_sliders_by_name(sim_info, slider_name)
    if not custom_sliders:
        output(f'Invalid Slider! \'{slider_name}\'')
        output('Available Sliders:')
        for custom_slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            output('>{}'.format(custom_slider.raw_display_name))
        return False
    custom_slider = next(iter(custom_sliders))
    if custom_slider is not None:
        output('Slider found.')
    else:
        output(f'Invalid Slider! \'{slider_name}\'')
        output('Available Sliders:')
        for custom_slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            output('>{}'.format(custom_slider.raw_display_name))
        return False
    CSFCustomSliderApplicationService().reset_slider(sim_info, custom_slider, trigger_event=True, persist_value=True)
    output('Success, Sliders reset.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    'csf.reset_sliders',
    'Reset all sliders on a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Name or ID', 'The Sim to modify.', is_optional=True, default_value='Active Sim'),
    ),
)
def _csf_reset_sliders(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    output('Resetting all sliders.')
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    output(f'Resetting all sliders for \'{sim_info}\'.')
    CSFCustomSliderApplicationService().reset_all_sliders(sim_info, persist_value=True)
    output('Success, Sliders reset.')
