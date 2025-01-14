# pyright: reportUnusedParameter=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportMissingTypeStubs=false

'''
This python script requires win11toast
'''

import obspython as obs # pyright: ignore[reportMissingImports]
from win11toast import notify, clear_toast
from enum import Enum

class OBSFrontendEvent(Enum):
    OBS_FRONTEND_EVENT_STREAMING_STARTING = 0
    OBS_FRONTEND_EVENT_STREAMING_STARTED = 1
    OBS_FRONTEND_EVENT_STREAMING_STOPPING = 2
    OBS_FRONTEND_EVENT_STREAMING_STOPPED = 3
    OBS_FRONTEND_EVENT_RECORDING_STARTING = 4
    OBS_FRONTEND_EVENT_RECORDING_STARTED = 5
    OBS_FRONTEND_EVENT_RECORDING_STOPPING = 6
    OBS_FRONTEND_EVENT_RECORDING_STOPPED = 7
    OBS_FRONTEND_EVENT_SCENE_CHANGED = 8
    OBS_FRONTEND_EVENT_SCENE_LIST_CHANGED = 9
    OBS_FRONTEND_EVENT_TRANSITION_CHANGED = 10
    OBS_FRONTEND_EVENT_TRANSITION_STOPPED = 11
    OBS_FRONTEND_EVENT_TRANSITION_LIST_CHANGED = 12
    OBS_FRONTEND_EVENT_SCENE_COLLECTION_CHANGED = 13
    OBS_FRONTEND_EVENT_SCENE_COLLECTION_LIST_CHANGED = 14
    OBS_FRONTEND_EVENT_PROFILE_CHANGED = 15
    OBS_FRONTEND_EVENT_PROFILE_LIST_CHANGED = 16
    OBS_FRONTEND_EVENT_EXIT = 17
    OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTING = 18
    OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTED = 19
    OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPING = 20
    OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPED = 21
    OBS_FRONTEND_EVENT_STUDIO_MODE_ENABLED = 22
    OBS_FRONTEND_EVENT_STUDIO_MODE_DISABLED = 23
    OBS_FRONTEND_EVENT_PREVIEW_SCENE_CHANGED = 24
    OBS_FRONTEND_EVENT_SCENE_COLLECTION_CLEANUP = 25
    OBS_FRONTEND_EVENT_FINISHED_LOADING = 26
    OBS_FRONTEND_EVENT_RECORDING_PAUSED = 27
    OBS_FRONTEND_EVENT_RECORDING_UNPAUSED = 28
    OBS_FRONTEND_EVENT_TRANSITION_DURATION_CHANGED = 29
    OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED = 30
    OBS_FRONTEND_EVENT_VIRTUALCAM_STARTED = 31
    OBS_FRONTEND_EVENT_VIRTUALCAM_STOPPED = 32
    OBS_FRONTEND_EVENT_TBAR_VALUE_CHANGED = 33
    OBS_FRONTEND_EVENT_SCENE_COLLECTION_CHANGING = 34
    OBS_FRONTEND_EVENT_PROFILE_CHANGING = 35
    OBS_FRONTEND_EVENT_SCRIPTING_SHUTDOWN = 36
    OBS_FRONTEND_EVENT_PROFILE_RENAMED = 37
    OBS_FRONTEND_EVENT_SCENE_COLLECTION_RENAMED = 38
    OBS_FRONTEND_EVENT_THEME_CHANGED = 39
    OBS_FRONTEND_EVENT_SCREENSHOT_TAKEN = 40

enabled = True

DESCRIPTION = '''
<center><h2>OBS Toast</h2></center>
<p>Display toast notifications for OBS events</p>
<p>Requires: <code style="color: lime">win11toast</code></p>
'''

# Description displayed in the Scripts dialog window
def script_description():
    return DESCRIPTION

# Called to set default values of data settings
def script_defaults(settings):
    obs.obs_data_set_default_bool(settings, "enabled", enabled)

# Called to display the properties GUI
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_bool(props, "enabled", "Enabled")
    return props

# Called after change of settings including once after script load
def script_update(settings):
  global enabled
  enabled = obs.obs_data_get_bool(settings, "enabled")

def when_enabled(func):
    global enabled
    def wrapper(data):
        global enabled
        print(f'Enabled: {enabled}')
        if enabled:
            func(data)
    return wrapper

@when_enabled
def output_start(data):
    clear_toast()
    _ = notify('Recording Started', 'Recording has started.')

@when_enabled
def output_stop(data):
    clear_toast()
    file_path:str = obs.obs_frontend_get_current_record_output_path()
    _ = notify(
        'Recording Stopped',
        f'Recording saved to {file_path}',
        buttons=[
            {'activationType': 'protocol', 'arguments': file_path, 'content': 'Play'},
            {'activationType': 'protocol', 'arguments': f'file:///{obs.obs_frontend_get_current_record_output_path()}', 'content': 'Open Folder'}
        ],
    )

@when_enabled
def output_pause(data):
    clear_toast()
    _ = notify('Recording Paused', 'Recording has paused.')

@when_enabled
def output_unpause(data):
    clear_toast()
    _ = notify('Recording Unpaused', 'Recording has resumed.')

@when_enabled
def replay_buffer_start(data):
    clear_toast()
    _ = notify('Replay Buffer Started', 'Replay buffer has started.')

@when_enabled
def replay_buffer_stop(data):
    clear_toast()
    _ = notify('Replay Buffer Stopped', 'Replay buffer has stopped.')

@when_enabled
def replay_buffer_save(data):
    clear_toast()
    file_path:str = obs.obs_frontend_get_last_replay()
    _ = notify(
        'Replay Buffer Saved',
        f'Replay buffer saved to {file_path}',
        buttons=[
            {'activationType': 'protocol', 'arguments': file_path, 'content': 'Play'},
            {'activationType': 'protocol', 'arguments': f'file:///{obs.obs_frontend_get_last_replay()}', 'content': 'Open Folder'}
        ],
    )

@when_enabled
def screenshot_taken(data):
    clear_toast()
    file_path:str = obs.obs_frontend_get_last_screenshot()
    _ = notify(
        'Screenshot Taken',
        f'Screenshot saved to {file_path}',
        image=f'file:///{file_path}',
    )

def front_end_callback(data: int):
    match data:
        case OBSFrontendEvent.OBS_FRONTEND_EVENT_RECORDING_STARTED.value:
            output_start(data)
        case OBSFrontendEvent.OBS_FRONTEND_EVENT_RECORDING_STOPPED.value:
            output_stop(data)
        case OBSFrontendEvent.OBS_FRONTEND_EVENT_RECORDING_PAUSED.value:
            output_pause(data)
        case OBSFrontendEvent.OBS_FRONTEND_EVENT_RECORDING_UNPAUSED.value:
            output_unpause(data)
        case OBSFrontendEvent.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTED.value:
            replay_buffer_start(data)
        case OBSFrontendEvent.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPED.value:
            replay_buffer_stop(data)
        case OBSFrontendEvent.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED.value:
            replay_buffer_save(data)
        case OBSFrontendEvent.OBS_FRONTEND_EVENT_SCREENSHOT_TAKEN.value:
            screenshot_taken(data)
        case _: pass

def script_load(settings):
    print('Script loading...')
    obs.obs_frontend_add_event_callback(front_end_callback)
    print('Script loaded.')

def script_unload():
    print('Script unloading...')
    obs.obs_frontend_remove_event_callback(front_end_callback)
    print('Script unloaded.')
