#!/usr/bin/env python
"""
weewx-bmp3xx
"""
import time
import busio
import board
import adafruit_bmp3xx
import weewx
from weewx.engine import StdService
import weeutil
import weeutil.logger
import logging

weeutil.logger.setup(__name__)
log = logging.getLogger(__name__)

def surely_a_list(innie):
    if isinstance(innie, list):
        return innie
    if innie is None or innie == "":
        return []
    return [innie] # cross fingers

class Bmp3xx(StdService):

    def __init__(self, engine, config_dict):

      # Initialize my superclass first:
      super(Bmp3xx, self).__init__(engine, config_dict)
      self.bmp3xx_dict = config_dict.get('Bmp3xx', {})
      log.info('bmp3xxwx configuration %s' % self.bmp3xx_dict)

      # TODO figure out how to sanely take these for the busio library
#      self.port = int(self.bmp3xx_dict.get('i2c_port', '1'))
      self.address = int(self.bmp3xx_dict.get('i2c_address', '0x77'), base=16)

      self.default_units = self.bmp3xx_dict.get('usUnits', 'US').upper()
      self.default_units = weewx.units.unit_constants[self.default_units]

      self.temperatureKeys = surely_a_list(self.bmp3xx_dict.get('temperatureKeys', 'inTemp'))
      self.temperature_must_have = surely_a_list(self.bmp3xx_dict.get('temperature_must_have', []))

      # The conversion from station pressure to MSL barometric pressure depends on the
      # temperature. So, the default is to only provide the pressure value when there
      # is already an outdoor temperature value
      self.pressureKeys = surely_a_list(self.bmp3xx_dict.get('pressureKeys', 'pressure'))
      self.pressure_must_have = surely_a_list(self.bmp3xx_dict.get('pressure_must_have', ['outTemp']))

      self.bus = busio.I2C(board.SCL, board.SDA)
      # this caches part-speciofic stuff so that a weewx restart is needed
      # if you change the bmp3xx sensor part; each one is unique
#      self.calibration_params = bmp3xx.load_calibration_params(self.bus, self.address)
      self.bmp = adafruit_bmp3xx.BMP3XX_I2C(self.bus, self.address)

      # TODO add oversampling support
      # 
#      bmp.pressure_oversampling = 8
#      bmp.temperature_oversampling = 2

#      loginf('I2C port: %s' % self.port)
      log.info('I2C address: %s' % hex(self.address))
      log.info('fallback default units: %s' % weewx.units.unit_nicknames[self.default_units])

      # This is last to make sure all the other stuff is ready to go
      # (avoid race condition)
      self.bind(weewx.NEW_LOOP_PACKET, self.new_loop_packet)
      
    def new_loop_packet(self, event):

        packet = event.packet

        log.debug('loop packet')

        # the sample method will take a single reading and return a
        # compensated_reading object
        bmp_pressure = self.bmp.pressure
        bmp_temperature = self.bmp.temperature

        # If there is a declared set of units already, we'll convert to that.
        # If there isn't, we'll accept the configured wisdom.
        if 'usUnits' in packet:
            converter = weewx.units.StdUnitConverters[packet['usUnits']]
        else:
            converter = weewx.units.StdUnitConverters[self.default_units]

        if all(must_have in packet for must_have in self.pressure_must_have):
            pressurePA = (bmp_pressure, 'mbar', 'group_pressure')
            converted = converter.convert(pressurePA)
            for key in self.pressureKeys:
                packet[key] = converted[0]

        if all(must_have in packet for must_have in self.temperature_must_have):
            temperatureC = (bmp_temperature, 'degree_C', 'group_temperature')
            converted = converter.convert(temperatureC)
            for key in self.temperatureKeys:
                packet[key] = converted[0]

        log.debug(packet)
