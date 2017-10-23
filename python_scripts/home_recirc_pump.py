# Checks the state of the recirculation pump and toggles it if
# it is not the current one according to the timetable

SCHEDULE = {datetime.time(16,00): 'on',
            datetime.time(23,30): 'off',
            datetime.time(7,00): 'on',
            datetime.time(9,00): 'off'}
SCHEDULE_WEEKEND = {datetime.time(7,00): 'on',
                    datetime.time(10,00): 'off',
                    datetime.time(16,00): 'on',
                    datetime.time(23,59): 'off'}

current_state = hass.states.get('sensor.current_state').state
if current_state != 'home':
    raise 'Wrong state for the script! Should be "home" is "{}"'.format(current_state)

is_workday = hass.states.get('binary_sensor.workday_sensor').state == 'on'
schedule = SCHEDULE if is_workday else SCHEDULE_WEEKEND
# Have to use this construct instead of sorted(schedule.keys()) :(
sorted_times = [k for k in schedule.keys()]
sorted_times.sort()
# Find the last event time that is before now
event_time = [t for t in sorted_times if datetime.datetime.now().time() >= t]
# Event time is latest before now or latest event in the day
# in case when now is between midnight and the first event in the morning
event_time = event_time[-1] if event_time else sorted_times[-1]
required_state = schedule[event_time]
pump_state = hass.states.get('switch.recirc_pump').state

logger.info('Pump state is "%s", required state is "%s"', pump_state, required_state)
# Turn off pump for 10 minutes if it has been on or flip it if states
# are not equal
if (required_state == 'on' and pump_state == 'on') or required_state != pump_state:
    hass.services.call('switch', 'toggle', {'entity_id': 'switch.recirc_pump'})
