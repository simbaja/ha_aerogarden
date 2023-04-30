# Home Assistant Aerogarden
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/simbaja/homeassistant-aerogarden/master.svg)](https://results.pre-commit.ci/latest/github/simbaja/homeassistant-aerogarden/master)


This is a custom component for [Home Assistant](http://home-assistant.io) that adds support for the Miracle Grow [AeroGarden](http://www.aerogarden.com) Wifi hydroponic gardens.


## Background
This was done without help from the AeroGarden people. As far as I can tell they post no public API. I took inspiration and code from the code in this [forum post by epotex](https://community.home-assistant.io/t/first-timer-trying-to-convert-a-working-script-to-create-support-for-a-new-platform).

Currently, the code is setup to query the AeroGarden servers every 30 seconds.

## Tested Models

* Harvest Wifi

(I expect other models to work, since this queries their cloud service not the garden directly)

## Setup
Copy contents of the custom_compents/aerogarden/ directory into your <HA-CONFIG>/custom_components/aerogarden directory (```/config/custom_components``` on hassio)

Your directory structure should look like this:

```
   config/custom_components/aerogarden/__init__.py
   config/custom_components/aerogarden/binary_sensor.py
   config/custom_components/aerogarden/sensor.py
   config/custom_components/aerogarden/light.py
```

## Configuration
Configuration is done through Home Assistant Config Flow in the UI.

## Data available
The component supports multiple gardens and multiple sensors will be created for each garden.  [GARDEN NAME] will be replaced by whatever you named the garden in the phone app.

### Light
* light.aerogarden_[GARDEN NAME]_light

### Binary Sensors (on/off)
* binary_sensor.aerogarden_[GARDEN NAME]_pump
* binary_sensor.aerogarden_[GARDEN NAME]_need_nutrients
* binary_sensor.aerogarden_[GARDEN NAME]_need_water

### Sensors
* sensor.aerogarden_[GARDEN NAME]_nutrient
* sensor.aerogarden_[GARDEN NAME]_planted

### Sample screenshot
![Screen Shot](https://raw.githubusercontent.com/simbaja/homeassistant-aerogarden/master/screen_shot.png)

## TODO
1. Code cleanup, this is my first HA component - it probably needs some work.
1. Turning on/off the light isn't working as smoothly as I hoped
