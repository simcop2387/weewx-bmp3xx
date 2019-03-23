#!/usr/bin/env python
"""
bme280wx
"""
import smbus2
import bme280
import syslog
import weewx
from weewx.engine import StdService
import weeutil

def logmsg(level, msg):
    syslog.syslog(level, 'bme280: %s' % msg)

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)

def surely_a_list(innie):
    if isinstance(innie, list):
        return innie
    if innie is None or innie is "":
        return []
    return [innie] # cross fingers

class Bme280wx(StdService):

    def __init__(self, engine, config_dict):

      # Initialize my superclass first:
      super(Bme280wx, self).__init__(engine, config_dict)
      self.bme280_dict = config_dict.get('Bme280wx', {})
      loginf('bme280wx configuration %s' % self.bme280_dict)

      self.port = int(self.bme280_dict.get('i2c_port', '1'))
      self.address = int(self.bme280_dict.get('i2c_address', '0x76'), base=16)

      self.default_units = self.bme280_dict.get('usUnits', 'US').upper()
      self.default_units = weewx.units.unit_constants[self.default_units]

      self.temperatureKeys = surely_a_list(self.bme280_dict.get('temperatureKeys', 'inTemp'))
      self.temperature_must_have = surely_a_list(self.bme280_dict.get('temperature_must_have', []))

      # The conversion from station pressure to MSL barometric pressure depends on the
      # temperature. So, the default is to only provide the pressure value when there
      # is already an outdoor temperature value
      self.pressureKeys = surely_a_list(self.bme280_dict.get('pressureKeys', 'pressure'))
      self.pressure_must_have = surely_a_list(self.bme280_dict.get('pressure_must_have', ['outTemp']))

      self.humidityKeys = surely_a_list(self.bme280_dict.get('humidityKeys', 'inHumidity'))
      self.humidity_must_have = surely_a_list(self.bme280_dict.get('humidity_must_have', []))
      
      self.bus = smbus2.SMBus(self.port)
      # this caches part-speciofic stuff so that a weewx restart is needed
      # if you change the bme280 sensor part; each one is unique
      self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

      loginf('I2C port: %s' % self.port)
      loginf('I2C address: %s' % self.address)
      loginf('fallback default units: %s' % weewx.units.unit_nicknames[self.default_units])

      # This is last to make sure all the other stuff is ready to go
      # (avoid race condition)
      self.bind(weewx.NEW_LOOP_PACKET, self.new_loop_packet)
      
    def new_loop_packet(self, event):

        packet = event.packet

        # the sample method will take a single reading and return a
        # compensated_reading object
        bme280data = bme280.sample(self.bus, self.address, self.calibration_params)
        loginf('BME280 data %s' % bme280data)

        if bme280data is None:
            return
        # If there is a declared set of units already, we'll convert to that.
        # If there isn't, we'll accept the configured wisdom.
        if 'usUnits' in packet:
            converter = weewx.units.StdUnitConverters[packet['usUnits']]
        else:
            converter = weewx.units.StdUnitConverters[self.default_units]

        if all(must_have in packet for must_have in self.pressure_must_have):
            pressurePA = (bme280data.pressure, 'mbar', 'group_pressure')
            converted = converter.convert(pressurePA)
            for key in self.pressureKeys:
                packet[key] = converted[0]

        if all(must_have in packet for must_have in self.temperature_must_have):
            temperatureC = (bme280data.temperature, 'degree_C', 'group_temperature')
            converted = converter.convert(temperatureC)
            for key in self.temperatureKeys:
                packet[key] = converted[0]

        if all(must_have in packet for must_have in self.humidity_must_have):
            humidityPCT = (bme280data.humidity, 'percent', 'group_percent')
            converted = converter.convert(humidityPCT)
            for key in self.humidityKeys:
                packet[key] = converted[0]

        logdbg(packet)
