# [bme280wx](https://gitlab.com/wjcarpenter/bme280wx)
_Copyright (c) 2019, WJCarpenter_
_[This project is licensed under the BSD 2-clause "Simplified" License.](https://gitlab.com/wjcarpenter/bme280wx/blob/master/LICENSE)_

bme280wx is an extension to [weewx weather station software](https://weewx.com).
It gives the ability to suplement existing station readings with temperature,
pressure, and humidity readings from a
[Bosch BME280 integrated environmental sensor](https://www.bosch-sensortec.com/bst/products/all_products/bme280).
BME280 sensors are widely available in inexpensive and convenient breakout boards from a variety of sources.
The extension assumes a Raspberry Pi environment, though it should be possible to run in other environments with some python programming work.
This extension always uses the I2C interface to read from the BME280 sensor.
Some BME280 sensor breakout boards also provide an SPI interface.

This interface seems to work correctly for a BMP280 as well,
if you happen to have one laying around. The humidity reading will be zero.
The other readings looked right to me,
but I didn't investigate whether they really were mathematically correct or just close enough.
It does _not_ work with BMP085.
The values are way off the mark.
It might be possible to tweak the conversions somehow, but I didn't explore it.
If you are using a BMP085, do yourself a favor and get a BME280.

## Installation
### Pre-requisites
* [weewx](https://weewx.com). Should work with any recent version. Tested with weewx 3.9.1.
* python 2.7 or later (but not python 3.x). You will already have a suitable python version if you are running weewx.
* [RPi.bme280](https://pypi.org/project/RPi.bme280/) python interface to the BME280 for a Raspberry Pi.
  The page at that link is also a great guide for wiring up your sensor if that's a new area for you.
  There are several other python libraries for the BME280, but they are not interchangable.

Download the compressed archive https://gitlab.com/wjcarpenter/bme280wx/-/archive/master/bme280wx-master.zip of this project to any convenient temporary directory.

Run the extensions installer:
```
wee_extension --install bme280wx-master.zip
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
    i2c_port = 1
    i2c_address = 0x76
    usUnits = US
    temperatureKeys = inTemp
    temperature_must_have = ""
    pressureKeys = pressure
    pressure_must_have = outTemp
    humidityKeys = inHumidity
    humidity_must_have = ""
```
(The items might be in a different order, which doesn't matter.)
There is a good chance that these defaults will work for you as-is.
You should at least check the values of `i2c_port` and `i2c_address`.
(If you are unsure how to do that, follow the guidance at [RPi.bme280](https://pypi.org/project/RPi.bme280/)
or [AdaFruit's Configuring I2C](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).)
These are the same as the defaults in the extension code,
so simply removing configuration items will not affect the defaults used by the extension.

The configuration items have the following meanings:

* `i2c_port`: The I2C port number. The default is `1`.
  Most Raspberry Pis use port number `1`, but some early models used port number `0`.
* `i2c_address`: The address of your BME280 sensor on the I2C interface.
  The default is `0x76`.
  This value must be in hex notation, as seen in the example.
  Most breakout boards use an address of `0x76` for BME280, but it is not guaranteed.
* `usUnits`: Ordinarily, a weewx loop data packet will contain a `usUnits` key identifying the units system for the values in the packet.
  The BME280 data will be converted to that units system before being added to the packet.
  It is possible that the loop data packet will not have the `usUnits` key.
  In that case, the BME280 data will be converted to the units system from this configuration item.
  Allowed values are `US` (the default), `METRIC`, or `METRICWX`,
  which are the units systems understood by weewx.
  A `usUnits` key with this value will _not_ be added to the weewx loop data packet.
* `temperatureKeys`: When the BME280 temperature data is added to weewx loop data packets, it will use this key or keys.
  If you don't want to use this BME280 value, set this to empty string (`""`).
  The value can be an empty string (meaning, do not add at all), a single item, or a comma-separated list of items.
  If multiple keys are configured, the same value is used with each key.
  The default is `inTemp` under the assumption that your Raspberry Pi is running indoors.
  _You should also make sure your BME280 sensor is at least a few inches away from the Raspberry Pi
  so that it's not affected by the heat of the running computer._
* `temperature_must_have`: The BME280 temperature will only be added to the weewx loop data packet if these items are already present in the packet.
  The value can be an empty string (meaning, no requirements), a single item, or a comma-separated list of items.
  The default is empty string.
* `pressureKeys`: When the BME280 pressure data is added to weewx loop data packets, it will use this key or keys.
  If you don't want to use this BME280 value, set this to empty string (`""`).
  The value can be an empty string (meaning, do not add at all), a single item, or a comma-separated list of items.
  If multiple keys are configured, the same value is used with each key.
  The default is `pressure`. Do _not_ use `barometer`.
  _This is "station pressure". The weewx software will calculate the MSL "barometric pressure" from this.
  That calculation depends upon the ambient temperature and the altitude._
  **Check to make sure that your weewx configuration reflects the altitude of your BME280 sensor, not that of other sensors you may have.**
* `pressure_must_have`: The BME280 pressure will only be added to the weewx loop data packet if these items are already present in the packet.
  The value can be an empty string (meaning, no requirements), a single item, or a comma-separated list of items.
  The default is `outTemp` because the calculation of MSL barometric pressure depends upon the ambient temperature.
  Although the pressure inside will be the same as the pressure outside, the temperature probably will not be.
* `humidityKeys`: When the BME280 humidity data is added to weewx loop data packets, it will use this key or keys.
  If you don't want to use this BME280 value, set this to empty string (`""`).
  The value can be an empty string (meaning, do not add at all), a single item, or a comma-separated list of items.
  If multiple keys are configured, the same value is used with each key.
  The default is `inHumidity`.
* `humidity_must_have`: The BME280 humidity will only be added to the weewx loop data packet if these items are already present in the packet.
  The value can be an empty string (meaning, no requirements), a single item, or a comma-separated list of items.
  The default is empty string.

After making any configuration changes, you must restart weewx.
Be sure to also have a look at the system log to see that weewx started properly.
Mistakes in configuration can lead to unrecoverable errors that prompt weewx to shut down.
