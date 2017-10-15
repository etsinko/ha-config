# This scrip must be run in 'home' mode and will adjust the shades
# depending on the current sun and darkness observations
# passed variables are:
# hass	The Home Assistant object. Access is only allowed to call services,
#       set/remove states and fire events.
# data	The data passed to the Python Script service call.
# logger


current_state = hass.states.get('sensor.current_state').state
if current_state != 'home':
    raise 'Wrong state for the script! Should be "home" is "{}"'.format(current_state)

# Sun's elevation below which the shades are closed
close_elevation = float(hass.states.get('input_number.close_shades_elevation').state)
# Sun's elevation above which the shades are open
open_elevation = float(hass.states.get('input_number.open_shades_elevation').state)
# Current sun elevation
sun_elevation = hass.states.get('sun.sun').attributes['elevation']
# Is it dark outside?
dark_outside = hass.states.get('binary_sensor.dark_outside').state
logger.info('Sun elevation is %.2f, Dark outside is "%s". Close Elevation = %.2f, Open Elevation = %.2f', sun_elevation, dark_outside, close_elevation, open_elevation)
# After sunset lower shades
if sun_elevation <= close_elevation:
    hass.services.call('notify', 'telegram_egor', {"message": "Sun is below horizon, closing shades."})
    hass.services.call('scene', 'turn_on', {"entity_id": ["scene.42453", # Dining Closed
                                                          "scene.54379", # Master Closed
                                                          "scene.56015", # Living Closed
                                                          ]})
# Raise shades after sunrise (cloudy)
elif sun_elevation >= open_elevation:
    if dark_outside == 'on':
        hass.services.call('notify', 'telegram_egor', {"message": "Sun is up! Although it is cloudy. Opening shades."})
        hass.services.call('scene', 'turn_on', {"entity_id": ["scene.37217", # Dining Vanes Open
                                                              "scene.37428", # Living Open
                                                              ]})
    # Raise shades after sunrise (sunny)
    else:
        hass.services.call('notify', 'telegram_egor', {"message": "Sun is up! Opening shades."})
        hass.services.call('scene', 'turn_on', {"entity_id": ["scene.37217", # Dining Vanes Open
                                                              "scene.43193", # Living Vanes Open
                                                              ]})
