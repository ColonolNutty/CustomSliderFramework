"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cncustomsliderframework.custom_slider_application_service import CSFCustomSliderApplicationService
from protocolbuffers import PersistenceBlobs_pb2
from server_commands.argument_helpers import get_optional_target, OptionalSimInfoParam
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


@Command('csf.apply_slider', command_type=CommandType.Live)
def _csf_apply_slider(slider_name: str, amount: float, opt_sim: OptionalSimInfoParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    output('Applying slider \'{}\' with amount \'{}\''.format(slider_name, amount))
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    output('Applying slider to \'{}\'.'.format(CommonSimNameUtils.get_full_name(sim_info)))
    facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
    facial_attributes.MergeFromString(sim_info.facial_attributes)
    from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
    custom_sliders = CSFSliderQueryUtils().get_sliders_by_name(sim_info, slider_name)
    if not custom_sliders:
        output('Invalid Slider! \'{}\''.format(slider_name))
        output('Available Sliders:')
        for custom_slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            output('>{}'.format(custom_slider.raw_display_name))
        return False
    custom_slider = next(iter(custom_sliders))
    if custom_slider is not None:
        output('Slider found.')
    else:
        output('Invalid Slider! \'{}\''.format(slider_name))
        output('Available Sliders:')
        for custom_slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            output('>{}'.format(custom_slider.raw_display_name))
        return False
    # noinspection PyBroadException
    try:
        amount = float(amount)
    except:
        output('Amount must be a number! \'{}\''.format(amount))
        return False
    output('Applying Sim Attributes!')
    return CSFCustomSliderApplicationService().apply_slider(sim_info, custom_slider, amount)


@Command('csf.help', command_type=CommandType.Live)
def _csf_help(opt_sim: OptionalSimInfoParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        output('Failed, No Sim found!')
        return
    output('Available Sliders:')
    from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
    for custom_slider in sorted(CSFSliderQueryUtils().get_sliders_for_sim(sim_info), key=lambda sl: sl.raw_display_name):
        output('>{}'.format(custom_slider.raw_display_name))
    output('Available Commands:')
    output('csf.apply_slider <slider_name> <amount>')
    output('    >|apply the slider with <slider_name> in the amount of <amount>')
    output('csf.reset_slider <slider_name>')
    output('    >|reset the slider with name <slider_name> to 0.0')
    output('csf.reset_sliders')
    output('    >|reset all sliders to 0.0')


@Command('csf.reset_slider', command_type=CommandType.Live)
def _csf_reset_slider(slider_name: str, opt_sim: OptionalSimInfoParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    output('Resetting slider \'{}\'.'.format(slider_name))
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    output('Resetting slider for \'{}\'.'.format(CommonSimNameUtils.get_full_name(sim_info)))
    from cncustomsliderframework.sliders.query.slider_query_utils import CSFSliderQueryUtils
    custom_sliders = CSFSliderQueryUtils().get_sliders_by_name(sim_info, slider_name)
    if not custom_sliders:
        output('Invalid Slider! \'{}\''.format(slider_name))
        output('Available Sliders:')
        for custom_slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            output('>{}'.format(custom_slider.raw_display_name))
        return False
    custom_slider = next(iter(custom_sliders))
    if custom_slider is not None:
        output('Slider found.')
    else:
        output('Invalid Slider! \'{}\''.format(slider_name))
        output('Available Sliders:')
        for custom_slider in CSFSliderQueryUtils().get_sliders_for_sim(sim_info):
            output('>{}'.format(custom_slider.raw_display_name))
        return False
    CSFCustomSliderApplicationService().reset_slider(sim_info, custom_slider)
    output('Success, Sliders reset.')


@Command('csf.reset_sliders', command_type=CommandType.Live)
def _csf_reset_sliders(opt_sim: OptionalSimInfoParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    output('Resetting all sliders.')
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        output('Failed, No Sim found!')
        return False
    output('Resetting all sliders for \'{}\'.'.format(CommonSimNameUtils.get_full_name(sim_info)))
    CSFCustomSliderApplicationService().reset_all_sliders(sim_info)
    output('Success, Sliders reset.')
