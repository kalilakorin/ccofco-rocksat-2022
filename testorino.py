sensors = {
    'MPL115A2': {
        'addr': 0x60,
        'type': 'temperature, pressure',
        'init': False
    },
    'BME280A': {
        'addr': 0x77,
        'type': 'outside temperature, pressure, humidity',
        'init': False
    },
    'BME280B': {
        'addr': 0x76,
        'type': 'inside temperature, pressure, humidity',
        'init': False
    },
    'VL53L1X': {
        'addr': 0x29,
        'type': 'distance',
        'init': False
    },
    'ADXL34X': {
        'addr': 0x53,
        'type': 'acceleration',
        'init': False
    }
}

for name in sensors:
    sensor = sensors[name]
    print(sensor['addr'])