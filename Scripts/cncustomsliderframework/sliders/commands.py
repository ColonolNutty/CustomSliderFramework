"""
This file is part of the Custom Slider Framework licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict

from cncustomsliderframework.modinfo import ModInfo
from cncustomsliderframework.sliders.slider_query_registry import CSFSliderQueryRegistry
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'csf_slider_query')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    'csf.log_slider_tags',
    'Show a list of all sliders by tags.',
)
def _csf_command_log_slider_tags(output: CommonConsoleCommandOutput):
    output('Logging Slider tags, this will take awhile and your game may freeze. Be Patient!')
    try:
        log.enable()
        slider_results = []
        for slider_tag_value in CSFSliderQueryRegistry()._slider_library.keys():
            sliders = CSFSliderQueryRegistry()._slider_library[slider_tag_value]
            count = len(sliders)
            slider_result = {
                'tag_type': str(slider_tag_value),
                'count': count,
            }
            slider_results.append(slider_result)
        sorted_sliders = sorted(slider_results, key=lambda res: res['tag_type'])
        log.debug('<Slider Tag>: <Count>')
        for slider in sorted_sliders:
            log.debug('{}: {}'.format(slider['tag_type'], slider['count']))
        log.disable()
        output('Slider Tags logged')
    except Exception as ex:
        log.error('Something happened', exception=ex)
        output('Failed to log Slider tags.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    'csf.log_slider_counts',
    'Show a list of all sliders by count.',
    command_arguments=(
        CommonConsoleCommandArgument('sliders_count', 'Number', 'Only sliders that are at or above this amount will show.', is_optional=True, default_value='5'),
    ),
)
def _csf_command_log_slider_counts(output: CommonConsoleCommandOutput, sliders_count: int = 5):
    output('Logging Sliders, this will take awhile and your game may freeze. Be Patient!')
    output('Will print pretty printed Sliders when the total count of them in a filter is less than {}'.format(sliders_count))
    try:
        log.enable()
        slider_results = []
        for (slider_tag_value, sliders) in CSFSliderQueryRegistry()._slider_library.items():
            count = len(sliders)
            slider_result = {
                'filter_key': slider_tag_value,
                'count': count,
                'sliders': tuple()
            }
            if count < sliders_count:
                slider_result['sliders'] = sliders
            slider_results.append(slider_result)
        sorted_sliders = sorted(slider_results, key=lambda res: res['filter_key'])
        for slider in sorted_sliders:
            log.format(filter_key=slider['filter_key'], count=slider['count'], sliders=slider['sliders'])
        log.disable()
        output('Sliders logged')
    except Exception as ex:
        log.error('Something happened', exception=ex)
        output('Failed to log.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    'csf.log_sliders_for_author',
    'Show a list of all sliders by an author.',
    command_arguments=(
        CommonConsoleCommandArgument('author', 'Author Name', 'The name of the author of the sliders.'),
    ),
)
def _csf_command_log_sliders_for_author(output: CommonConsoleCommandOutput, author: str):
    output('Logging Sliders, this will take awhile and your game may freeze. Be Patient!')
    if author is None:
        output('Please specify an author to locate Sliders for.')
        return
    output('Will print pretty printed Sliders when the author is the one specified {} (It wont work for authors with spaces in their names).'.format(author))
    try:
        log.enable()
        sliders_to_log: Dict[str, Any] = {}
        for (slider_tag_value, sliders) in CSFSliderQueryRegistry()._slider_library.items():
            for slider in sliders:
                if str(author).lower() != str(slider.author).lower():
                    continue
                slider_identifier = str(slider.unique_identifier)
                if slider_identifier in sliders_to_log:
                    if slider_tag_value in sliders_to_log[slider_identifier]['filter_keys']:
                        continue
                    sliders_to_log[slider_identifier]['filter_keys'].append(slider_tag_value)
                    continue
                sliders_to_log[slider_identifier] = {
                    'slider': slider,
                    'filter_keys': [slider_tag_value]
                }
        log.debug('Logging Sliders for author {}:'.format(author))
        for (key, val) in sliders_to_log.items():
            log.format(slider=val['slider'], filter_keys=val['filter_keys'])
        log.disable()
        output('Sliders logged')
    except Exception as ex:
        log.error('Something happened', exception=ex)
        output('Failed to log.')
