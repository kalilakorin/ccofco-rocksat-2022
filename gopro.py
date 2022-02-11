from goprocam import GoPro

with GoPro() as gopro:
    print("Yay! I'm connected via BLE, Wifi, initialized, and ready to send / get data now!")
    # Send some commands now