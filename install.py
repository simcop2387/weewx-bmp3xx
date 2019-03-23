# installer for bme280wx extension

from setup import ExtensionInstaller

def loader():
    return Bme280wxInstaller()

class Bme280wxInstaller(ExtensionInstaller):
    def __init__(self):
        super(Bme280wxInstaller, self).__init__(
            version="1.0",
            name='bme280wx',
            description='Add bme280 sensor readings to loop packet data',
            author="WJCarpenter",
            author_email="bill-bme280wx@carpenter.org",
            data_services='user.bme280wx.Bme280wx',
            config={
                'Bme280wx': {
                    'i2c_port': '1',
                    'i2c_address': '0x76',
                    'temperature': 'inTemp',
                    'temperature_must_have': '',
                    'pressure': 'pressure',
                    'pressure_must_have': 'outTemp',
                    'humidity': 'inHumidity',
                    'humidity_must_have': ''
                }
            },
            files=[('bin/user', ['bin/user/bme280wx.py'])]
            )
