# [bmp3xx](https://gitlab.com/simcop2387/weewx-bmp3xx)
_Copyright (c) 2021, Ryan Voots
_[This project is licensed under the BSD 2-clause "Simplified" License.](https://gitlab.com/wjcarpenter/bme280wx/blob/master/LICENSE)_

Based on the original project bme280wx from WJCarpenter, changed for the bmp3xx family of sensors

_Copyright (c) 2019, WJCarpenter_
_[This project is licensed under the BSD 2-clause "Simplified" License.](https://gitlab.com/wjcarpenter/bme280wx/blob/master/LICENSE)_
[bme280wx](https://gitlab.com/wjcarpenter/bme280wx)

bmp3xx is an extension to [weewx weather station software](https://weewx.com).
It gives the ability to suplement existing station readings with temperature,
pressure, and humidity readings from a
[Bosch BMP380 integrated pressure sensor](https://www.bosch-sensortec.com/bst/products/all_products/bmp380).
BMP380 sensors are widely available in inexpensive and convenient breakout boards from a variety of sources.
The extension assumes a Raspberry Pi environment, though it should be possible to run in other environments with some python programming work.
This extension always uses the I2C interface to read from the BMP280 sensor.
Some BMP280 sensor breakout boards also provide an SPI interface.

## Installation
### Pre-requisites
* [weewx](https://weewx.com). Should work with any recent version. Tested with weewx 3.9.1 and 4.1.0.
* python 2.7 or python 3.x. You will already have a suitable python version if you are running weewx.
* [adafruit-circuitpython-bmp3xx](https://github.com/adafruit/Adafruit_CircuitPython_BMP3XX) python interface to the BMP3xx for a Raspberry Pi.
* NOTE: If you are running weewx inside a Docker container, you must expose your I2C device 
  (`/dev/i2c-0` or `/dev/i2c-1`) to that container.

Download the compressed archive https://github.com/simcop2387/weewx-bmp3xx/archive/master.zip of this project to any convenient temporary directory.

Run the extensions installer:
```
wee_extension --install bmp3xx-master.zip
```
Restart weewx using these steps or your favorite local variant:
```
sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start
```
It's OK to delete the downloaded file after installation.
You will not need it for uninstalling the extension, but, of course, you will need it to re-install.

## Uninstall

To uninstall this extension, use the extensions installer:
```
wee_extension --uninstall bme280wx
```
Restart weewx using these steps or your favorite local variant:
```
sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start
```
## Upgrade
If you want to upgrade to a newer version of this extension,
simply uninstall the old version and install the new version, as noted above.
However, during the uninstall, the extension manager will remove the configuration settings (described in the next section).
If you have modified any of them, make a note of them before the uninstall.
(One easy way to do that is to simply rename the `[Bme280wx]` section to something else.
That will prevent the extension manager from removing the whole section.)

## Configuration
Installation will add a default configuration to `/etc/weewx/weewx.conf`:
```
# Options for extension 'bme280wx'
[Bme280wx]
    i2c_address = 0x77
    usUnits = US
    temperatureKeys = inTemp
    temperature_must_have = ""
    pressureKeys = pressure
    pressure_must_have = outTemp
```
(The items might be in a different order, which doesn't matter.)
There is a good chance that these defaults will work for you as-is.
You should at least check the values of `i2c_port` and `i2c_address`.
(If you are unsure how to do that, follow the guidance at [RPi.bme280](https://pypi.org/project/RPi.bme280/)
or [AdaFruit's Configuring I2C](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).)
These are the same as the defaults in the extension code,
so simply removing configuration items will not affect the defaults used by the extension.

The configuration items have the following meanings:

* `i2c_address`: The address of your BMP380 sensor on the I2C interface.
  The default is `0x77`.
  This value must be in hex notation, as seen in the example.
  Most breakout boards use an address of `0x76` for BME280, but it is not guaranteed.
* `usUnits`: Ordinarily, a weewx loop data packet will contain a `usUnits` key identifying the units system for the values in the packet.
  The BMP380 data will be converted to that units system before being added to the packet.
  It is possible that the loop data packet will not have the `usUnits` key.
  In that case, the BMP380 data will be converted to the units system from this configuration item.
  Allowed values are `US` (the default), `METRIC`, or `METRICWX`,
  which are the units systems understood by weewx.
  A `usUnits` key with this value will _not_ be added to the weewx loop data packet.
* `temperatureKeys`: When the BMP380 temperature data is added to weewx loop data packets, it will use this key or keys.
  If you don't want to use this BMP380 value, set this to empty string (`""`).
  The value can be an empty string (meaning, do not add at all), a single item, or a comma-separated list of items.
  If multiple keys are configured, the same value is used with each key.
  The default is `inTemp` under the assumption that your Raspberry Pi is running indoors.
  _You should also make sure your BMP380 sensor is at least a few inches away from the Raspberry Pi
  so that it's not affected by the heat of the running computer._
* `temperature_must_have`: The BMP380 temperature will only be added to the weewx loop data packet if these items are already present in the packet.
  The value can be an empty string (meaning, no requirements), a single item, or a comma-separated list of items.
  The default is empty string.
* `pressureKeys`: When the BMP380 pressure data is added to weewx loop data packets, it will use this key or keys.
  If you don't want to use this BME380 value, set this to empty string (`""`).
  The value can be an empty string (meaning, do not add at all), a single item, or a comma-separated list of items.
  If multiple keys are configured, the same value is used with each key.
  The default is `pressure`. Do _not_ use `barometer`.
  _This is "station pressure". The weewx software will calculate the MSL "barometric pressure" from this.
  That calculation depends upon the ambient temperature and the altitude._
  **Check to make sure that your weewx configuration reflects the altitude of your BME280 sensor, not that of other sensors you may have.**
* `pressure_must_have`: The BMP380 pressure will only be added to the weewx loop data packet if these items are already present in the packet.
  The value can be an empty string (meaning, no requirements), a single item, or a comma-separated list of items.
  The default is `outTemp` because the calculation of MSL barometric pressure depends upon the ambient temperature.
  Although the pressure inside will be the same as the pressure outside, the temperature probably will not be.

After making any configuration changes, you must restart weewx.
Be sure to also have a look at the system log to see that weewx started properly.
Mistakes in configuration can lead to unrecoverable errors that prompt weewx to shut down.
