# installer for bmp3xx extension
# Based on the Bme280wx extension by WJCarpenter

from setup import ExtensionInstaller

def loader():
    return Bmp3xxInstaller()

class Bmp3xxInstaller(ExtensionInstaller):
    def __init__(self):
        super(Bmp3xxInstaller, self).__init__(
            version="1.0",
            name='bmp3xx',
            description='Add bmp3xx sensor readings to loop packet data',
            author="Simcop2387",
            author_email="simcop2387@simcop2387.info",
            data_services='user.bmp3xx.Bmp3xx',
            config={
                'Bmp3xx': {
                    'i2c_port': '1',
                    'i2c_address': '0x76',
                    'usUnits': 'US',
                    'temperatureKeys': 'inTemp',
                    'temperature_must_have': '',
                    'pressureKeys': 'pressure',
                    'pressure_must_have': 'outTemp',
                    'humidityKeys': 'inHumidity',
                    'humidity_must_have': ''
                }
            },
            files=[('bin/user', ['bin/user/bmp3xx.py'])]
            )
