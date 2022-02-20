import time
from open_gopro import GoPro, Params

with GoPro() as gopro:
    gopro.ble_command.load_preset(Params.Preset.MAX_VIDEO)
    gopro.ble_setting.resolution.set(Params.Resolution.RES_5_3_K)
    gopro.ble_setting.fps.set(Params.FPS.FPS_30)
    gopro.ble_command.set_shutter(Params.Shutter.ON)
    time.sleep(2) # Record for 2 seconds
    gopro.ble_command.set_shutter(Params.Shutter.OFF)