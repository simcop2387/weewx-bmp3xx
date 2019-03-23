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

## Installation
### Pre-requisites
* [weewx](https://weewx.com). Should work with any recent version. Tested with weewx 3.9.1.
* python 2.7 or later (but not python 3.x). You will already have a suitable python version if you are running weewx.
* [RPi.bme280](https://pypi.org/project/RPi.bme280/) python interface to the BME280 for a Raspberry Pi.
  The page at that link is also a great guide for wiring up your sensor if that's new a new area for you.
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

## Configuration
Installation will add a default configuration to `/etc/weewx/weewx.conf`:
```
# Options for extension 'bme280wx'
[Bme280wx]
    i2c_port = 1
    i2c_address = 0x76
    temperatureKey = inTemp
    temperature_must_have = ""
    pressureKey = pressure
    pressure_must_have = outTemp
    humidityKey = inHumidity
    humidity_must_have = ""
```
(The items might be in a different order, which doesn't matter.)
There is a good chance that these defaults will work for you as-is.
You should at least check the values of `i2c_port` and `i2c_address`.
(If you are unsure how to do that, follow the guidance at [RPi.bme280](https://pypi.org/project/RPi.bme280/)
or [AdaFruit's Configuring I2C](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).)
These are the same as the defaults in the extension code,
so simply removing items will not remove the defaults.

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
  In that case, the BME280 data will be converted to the units system from this config item.
  Possible values are `US` (the default), `METRIC`, or `METRICWX`,
  which are the units systems understood by weewx.
  A `usUnits` key with this value will _not_ be added to the weewx loop data packet.
* `temperatureKey`: When the BME280 temperature data is added to weewx loop data packets, it will use this key.
  If you don't want to use this BME280 value, set this to empty string (`""`).
  The default is `inTemp` under the assumption that your Raspberry Pi is running indoors.
  _You should also make sure your BME280 sensor is at least a few inches away from the Raspberry Pi
  so that it's not affected by the heat of the running computer._
* `temperature_must_have`: The BME280 temperature will only be added to the weewx loop data packet if these items are already present in the packet.
  The value can be an empty string (meaning, no requirements), a single item, or a comma-separated list of items.
  The default is empty string.
* `pressureKey`: When the BME280 pressure data is added to weewx loop data packets, it will use this key.
  If you don't want to use this BME280 value, set this to empty string (`""`)
  The default is `pressure`. Do _not_ use `barometer`.
  _This is "station pressure". The weewx software will calculate the MSL "barometric pressure" from this.
  That calculation depends upon the ambient temperature and the altitude._
  **Check to make sure that your weewx configuration reflects the altitude of your BME280 sensor, not that of other sensors you may have.**
* `pressure_must_have`: The BME280 pressure will only be added to the weewx loop data packet if these items are already present in the packet.
  The value can be an empty string (meaning, no requirements), a single item, or a comma-separated list of items.
  The default is `outTemp` because the calculation of MSL barometric pressure depends upon the ambient temperature.
  Although the pressure inside will be the same as the pressure outside, the temperature probably will not be.
* `humidityKey`: When the BME280 humidity data is added to weewx loop data packets, it will use this key.
  If you don't want to use this BME280 value, set this to empty string (`""`)
  The default is `inHumidity`.
* `humidity_must_have`: The BME280 humidity will only be added to the weewx loop data packet if these items are already present in the packet.
  The value can be an empty string (meaning, no requirements), a single item, or a comma-separated list of items.
  The default is empty string.
