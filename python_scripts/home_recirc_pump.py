# Checks the state of the recirculation pump and toggles it if
# it is not the current one according to the timetable

SCHEDULE = {datetime.time(16,00): 'on',
            datetime.time(23,30): 'off',
            datetime.time(7,00): 'on',
            datetime.time(9,00): 'off'}

current_state = hass.states.get('sensor.current_state').state
if current_state != 'home':
    raise 'Wrong state for the script! Should be "home" is "{}"'.format(current_state)

# Have to use this construct instead of sorted(TIMETABLE.keys()) :(
sorted_times = [k for k in SCHEDULE.keys()]
sorted_times.sort()
# Find the last event time that is before now
event_time = [t for t in sorted_times if datetime.datetime.now().time() >= t]
# Event time is latest before now or latest event in the day
# in case when now is between midnight and the first event in the morning
event_time = event_time[-1] if event_time else sorted_keys[-1]

required_state = TIMETABLE[event_time]
pump_state = hass.states.get('switch.recirc_pump').state
logger.info('Pump state is "%s", required state is "%s"', pump_state, required_state)
if required_state != pump_state:
    hass.services.call('switch', 'toggle', {'entity_id': 'switch.recirc_pump'})
