from cncustomsliderframework.modinfo import ModInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_changed_occult_type import S4CLSimChangedOccultTypeEvent
from sims4communitylib.events.sim.events.sim_spawned import S4CLSimSpawnedEvent


# @CommonEventRegistry.handle_events(ModInfo.get_identity())
def _csf_refresh_sliders_on_sim_load(event_data: S4CLSimSpawnedEvent):
    from cncustomsliderframework.custom_slider_application_service import CSFCustomSliderApplicationService
    CSFCustomSliderApplicationService().reapply_all_sliders(event_data.sim_info)


# @CommonEventRegistry.handle_events(ModInfo.get_identity())
def _csf_refresh_sliders_on_sim_occult_changed(event_data: S4CLSimChangedOccultTypeEvent):
    from cncustomsliderframework.custom_slider_application_service import CSFCustomSliderApplicationService
    CSFCustomSliderApplicationService().reapply_all_sliders(event_data.sim_info)
