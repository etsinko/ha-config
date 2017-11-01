# ha-config

My current Home Assistant setup:

1. Insteon Lights and Dimmers
2. MyQ Liftmaster garage door opener
3. Envisalink connected alarm
4. Ring doorbell
5. Ecobee thermostats
6. Hunter Douglas powerview shades
7. Security cameras + Xeoma server
8. Plex server
9. Monoprice 6-zone amplifier

# Description

The main idea behind my automation is that Home Assistant maintans a simple state machine defined by template sensor `current_state`. This sensor can have 4 possible states:

- `home` - this state means that somebody is home therefore all automations for occupied house should be activated, i.e. hot water recirculation pump, turning all lights off at night, maintaining comfortable temperature and closing or opening blinds depending on light outside.
- `on_vacation` - this state means that nobody is at home for a long period of time (more than a couple of days). In this state temperature is lowered, blinds closed and all lights are turned off. In addition security is enforced.
- `away` - this state is for short-term leaves. Right now it is very similar to `on_vacation` state.
- `have_guests` - this is a special state that indicates that there we are having guest staying with us. In this state presence detection based automations are turned off because there might be cases when we are not home but the guests are.

`on_vacation` or `have_guests` states are controlled by `input_select.system_mode` while `home` or `away` states are chosen automatically by Home Assistant based on bayesian binary sensor `somebody_home`. The simple algorithm that defines value for `current_state` sensor is as follows:

```
If `input_select.system_mode` is `On Vacation` then `current_state` = `on_vacation`
else if `input_select.system_mode` is `Have guests` then `current_state` = `have_guests`
else if `binary_sensor.somebody_home` is `on` then `current_state` = `home`
else `current_state` = `away`
```

Implementing such a state machine allows me to create individual automations for transitions between states. I.e. there is an automation for a case when `current_state` switches from `home` to `away`. This automation turns off all lights, closes all shades and turns off hot water recirculation pump.

Each state automations are stored in `automations` directory under their respective name. For example automations for `home` state are in `automations/home`. The automations for transitions between states are stored in `from_"state_name".yaml` files. For example automation that happens when state is changed from `away` to `home` is stored in `automations/home/from_away.yaml` while automation for the transition from `home` to `away` is stored in `automations/away/from_home.yaml`
