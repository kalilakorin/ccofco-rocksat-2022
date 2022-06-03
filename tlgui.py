#!/usr/bin/env python

"""

 ** pre-release version **

 * BETA0.95 * Python tinyLiDAR Terminal GUI for use with the Raspberry Pi 3
 To be used at the shell/command line terminal
 {PuTTY SSH port 22 default 80x24 window size, UTF-8 remote char set}

 run as 'python tlgui.py'

 Dec 29 2017 by Dinesh Bhatia
 Public Domain

Notes:

 Use 'sudo killall pigpiod' if you get 'GPIO already in use' error at next launch

 Cut the shorting traces in the pull-up resistor pads on each tinyLiDAR if using
  the I2C Port 1 on Raspberry Pi 3. These are gpio pins 2, 3 since the pi has built-in 1.8K
  pull-ups.

"""

from subprocess import Popen, PIPE
import sys
import tl_variables as tlv
import tinyLiDAR as tl

tl.printMenu()
tl.printMenu1()

while True:
    commandEntered = tl.input_func(u"> ")
    tl.printMenu()
    tl.printMenu1()
    i = commandEntered.upper()

    if i == 'Z': break

    if commandEntered == '':  # default command if only enter is pressed
        print(u" [default] Command 'D' to 0x%X" % tlv.I2C_Address)
        tl.Dcommand(1, 0, tlv.I2C_Address)
        continue

    elif i == 'RESET':
        print(" %s" % tlv.tinyLiDAR_commands['RESET'])
        tlv.I2C_Address = tlv.default_tinyLiDAR_address  # set to default I2C addr if no value entered
        tl.writeCommand(0, '\6')
        print(": Please wait for reboot")
        tl.delay(tlv.rebootTime)  # wait for reboot to continue
        print(": Done. ")
        continue

    elif i.startswith('I'):
        print(" %s" % tlv.tinyLiDAR_commands['I'])
        # print(": change the Terminal's I2C address.")
        if (i == "I"):
            tlv.I2C_Address = tlv.default_tinyLiDAR_address  # set to default I2C addr if no value entered
            print(" --> New I2C Address for Terminal = 0x%X" % tlv.I2C_Address)
        else:
            tlv.I2C_Address = int(i[1:len(i)], 16)
            print(" --> New I2C Address for Terminal = 0x%X" % tlv.I2C_Address)
        continue

    elif i.startswith('R'):
        print(" %s" % tlv.tinyLiDAR_commands['R'])
        if (i == "R"):
            i2cAdr = tlv.default_tinyLiDAR_address  # set to default I2C addr if no value entered
            print(" --> New I2C Address for tinyLiDAR = 0x%X" % i2cAdr)
        else:
            i2cAdr = int(i[1:len(i)], 16)
            print(" --> New I2C Address for tinyLiDAR = 0x%X" % i2cAdr)
        tl.writeCommand2(tlv.I2C_Address, "R", i2cAdr)

        continue

    elif i.startswith('W'):
        tl.printMenu()
        sys.stdout.write(u"\u001b[1B: change VL53L0 parameters.")

        if (i == "W"):  # set to default if no values are entered

            param = []
            param.append((tlv.SignalRateLimit & 0xff00) >> 8)  # MSB
            param.append(tlv.SignalRateLimit)  # LSB
            param.append(tlv.SignalEstimateLimit)
            param.append((tlv.TimingBudget & 0xff00) >> 8)  # MSB
            param.append(tlv.TimingBudget)  # LSB
            param.append(tlv.VCELperiod)
            print("\n\r\n\r:  Using Default Values - ")

            i = (param[0] * 256 + param[1]) / 100.0
            print("   SignalLimit = %0.2f Mcps" % i)

            print("   SigmalLimit = %d mm" % param[2])

            i = (param[3] * 256 + param[4])
            print("   timeBudget = %d ms" % i)

            if (param[5] == 14):
                print("   preRangeVcselPeriod = 14 ")
                print("   finalRangeVcselPeriod = 10 ")
            elif (param[5] == 18):
                print("   preRangeVcselPeriod = 18 ")
                print("   finalRangeVcselPeriod = 14 ")

        else:
            param = []

            print("\n\r\n\r The values you entered were - ")

            i = i.split(" ")

            print("   SignalLimit = %0.2f Mcps" % float(int(i[1]) / 100.0))
            param.append((int(i[1]) & 0xff00) >> 8)  # MSB
            param.append(int(i[1]) & 0x00ff)  # LSB

            print("   SigmalLimit = %d mm" % int(i[2]))
            param.append(int(i[2]))

            print("   timeBudget = %d ms" % int(i[3]))
            param.append((int(i[3]) & 0xff00) >> 8)  # MSB
            param.append(int(i[3]) & 0x00ff)  # LSB

            if (int(i[4]) == 14):
                print("   preRangeVcselPeriod = 14 ")
                print("   finalRangeVcselPeriod = 10 ")
            elif (int(i[4]) == 18):
                print("   preRangeVcselPeriod = 18 ")
                print("   finalRangeVcselPeriod = 14 ")

            param.append(int(i[4]))

        if (tl.confirm()):
            print(": Now writing parameters to tinyLiDAR. \n\r")

            tl.writeCommand(tlv.I2C_Address, "MS")  # set to SS mode
            tl.delay(tlv.rebootTime)  # wait for reboot to continue

            tl.Wcommand(tlv.I2C_Address, param)
            tl.delay(tlv.rebootTime)  # wait for reboot to continue

            print("> Done. \n\r")

        else:
            commandEntered = raw_input(u"\u001b[1B> Press ENTER 2x to Continue ")

        continue

    elif i in tlv.tinyLiDAR_commands:

        if i == 'T0':
            print(" %s" % tlv.tinyLiDAR_commands['T0'])
            tl.writeCommand(tlv.I2C_Address, "T0")
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            continue

        elif i == 'T1':
            print(" %s" % tlv.tinyLiDAR_commands['T1'])
            tl.writeCommand(tlv.I2C_Address, "T1")
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            continue

        elif i == 'CD':

            tl.printMenu()
            sys.stdout.write(u"\u001b[1B: Perform Offset Cal at a distance of = %d" % tlv.cal_offset_distance + " mm")

            tl.writeCommand(tlv.I2C_Address, "T0")  # turn off the WDT
            tl.delay(tlv.rebootTime)  # wait for reboot to continue

            print

            tl.writeCommand(tlv.I2C_Address, "PH")  # set to high accuracy preset
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            tl.writeCommand(tlv.I2C_Address, "MC")  # set to continuous mode
            tl.delay(tlv.rebootTime)  # wait for reboot to continue

            print(" Distance Before Cal: ")

            for i in range(0, 10):

                Measured_Distance = tl.Read_Distance(tlv.I2C_Address)

                if (Measured_Distance):
                    print(u" Distance = %d mm" % Measured_Distance)
                else:
                    print(" - ")  # invalid distance data will show as '-'

                tl.delay(205)  # need 200ms at least so give a bit extra

            caloffset = []
            caloffset.append(tlv.cal_offset_distance >> 8 & 0x00ff)  # need to break up the 16bit xtalk distance value
            caloffset.append(tlv.cal_offset_distance & 0x00ff)
            tl.CDcommand(tlv.I2C_Address, caloffset)

            print("\n\r **** Calibrating Now - Please wait approx 10sec **** \n\r")

            tl.delay(11000)  # give it over 10sec to calibrate now

            tl.writeCommand(tlv.I2C_Address, "X")  # reboot tinyLiDAR
            tl.delay(tlv.rebootTime)  # wait for reboot to continue

            print(" Distance After Cal: ")

            for i in range(0, 10):

                Measured_Distance = tl.Read_Distance(tlv.I2C_Address)

                if (Measured_Distance):
                    print(u" Distance = %d mm" % Measured_Distance)
                else:
                    print(" - ")  # invalid distance data will show as '-'

                tl.delay(205)  # need 200ms at least so give a bit extra

            tl.writeCommand(tlv.I2C_Address, "MS")  # set to single step mode again
            tl.delay(tlv.rebootTime)  # wait for reboot to continue

            print("\n\r **** Cal Complete **** Press Enter to Continue")

            continue

        elif i == 'CX':

            tl.printMenu()
            sys.stdout.write(u"\u001b[1B: Perform Crosstalk Cal at a distance of = %d" % tlv.cal_xtalk_distance + " mm")

            tl.writeCommand(tlv.I2C_Address, "T0")  # turn off the WDT
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            print

            tl.writeCommand(tlv.I2C_Address, "PH")  # set to high accuracy preset
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            tl.writeCommand(tlv.I2C_Address, "MC")  # set to continuous mode
            tl.delay(tlv.rebootTime)  # wait for reboot to continue

            print(" Distance Before Cal: ")

            for i in range(0, 10):

                Measured_Distance = tl.Read_Distance(tlv.I2C_Address)

                if (Measured_Distance):
                    print(u" Distance = %d mm" % Measured_Distance)
                else:
                    print(" - ")  # invalid distance data will show as '-'

                tl.delay(205)  # need 200ms at least so give a bit extra

            caloffset = []
            caloffset.append(tlv.cal_xtalk_distance >> 8 & 0x00ff)  # need to break up the 16bit xtalk distance value
            caloffset.append(tlv.cal_xtalk_distance & 0x00ff)
            tl.CXcommand(tlv.I2C_Address, caloffset)

            print("\n\r **** Calibrating Now - Please wait approx 10sec **** \n\r")

            tl.delay(11000)  # give it over 10sec to calibrate now

            tl.writeCommand(tlv.I2C_Address, "X")  # reboot tinyLiDAR
            tl.delay(tlv.rebootTime)  # wait for reboot to continue

            print(" Distance After Cal: ")

            for i in range(0, 10):

                Measured_Distance = tl.Read_Distance(tlv.I2C_Address)

                if (Measured_Distance):
                    print(u" Distance = %d mm" % Measured_Distance)
                else:
                    print(" - ")  # invalid distance data will show as '-'

                tl.delay(205)  # need 200ms at least so give a bit extra

            tl.writeCommand(tlv.I2C_Address, "MS")  # set to single step mode again
            tl.delay(tlv.rebootTime)  # wait for reboot to continue

            print("\n\r **** Cal Complete **** Press Enter to Continue")
            continue


        elif i == 'D':
            print(" %s" % tlv.tinyLiDAR_commands['D'])
            tl.Dcommand(1, 0, tlv.I2C_Address)
            continue

        elif i == 'DC':
            tl.ContinuousReadingForTerminal(tlv.I2C_Address)
            continue

        elif i == 'E':
            print(" %s" % tlv.tinyLiDAR_commands['E'])
            tl.writeCommand(tlv.I2C_Address, "E")
            continue

        elif i == 'F':
            print(" %s" % tlv.tinyLiDAR_commands['F'])
            tl.writeCommand(tlv.I2C_Address, "F")
            continue

        elif i == 'G':
            print(" %s" % tlv.tinyLiDAR_commands['G'])
            tl.writeCommand(tlv.I2C_Address, "G")
            continue

        elif i == 'MC':
            print(" %s" % tlv.tinyLiDAR_commands['MC'])
            tl.writeCommand(tlv.I2C_Address, "MC")
            tl.delay(tlv.rebootTime)  # wait for reboot to continue

            # please wait for reboot - print something here? -- dindin

            continue

        elif i == 'MS':
            print(" %s" % tlv.tinyLiDAR_commands['MS'])
            tl.writeCommand(tlv.I2C_Address, "MS")
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            continue

        elif i == 'PL':
            print(" %s" % tl.tinyLiDAR_commands['PL'])
            tl.writeCommand(tlv.I2C_Address, "PL")
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            continue

        elif i == 'PH':
            print(" %s" % tlv.tinyLiDAR_commands['PH'])
            tl.writeCommand(tlv.I2C_Address, "PH")
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            continue

        elif i == 'PS':
            print(" %s" % tlv.tinyLiDAR_commands['PS'])
            tl.writeCommand(tlv.I2C_Address, "PS")
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            continue

        elif i == 'PT':
            print(" %s" % tlv.tinyLiDAR_commands['PT'])
            tl.writeCommand(tlv.I2C_Address, "PT")
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            continue

        elif i == 'X':
            print(" %s" % tlv.tinyLiDAR_commands['X'])
            tl.writeCommand(tlv.I2C_Address, "X")
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            continue

        elif i == 'Y':
            print(" %s" % tlv.tinyLiDAR_commands['Y'])
            tl.writeCommand(tlv.I2C_Address, "Y")
            tl.delay(tlv.rebootTime)  # wait for reboot to continue
            continue

        elif i == 'Q':
            (count, data) = tl.Qcommand(tlv.I2C_Address);
            tl.printMenu()
            sys.stdout.write(u"\u001b[1B  Current Operation Mode is: ")

            if (data[0] == 0x43):
                print(u"\u001b[1mContinuous\u001b[0m")
            elif (data[0] == 0x53):
                print(u"\u001b[1mSingleStep\u001b[0m")
            elif (data[0] == 0x4c):
                print(u"\u001b[1mUltraLowPower\u001b[0m")

            if ((data[14] & 0x01) == 0):
                print(u"  WatchDog Timer: \u001b[1mOFF\u001b[0m")
            else:
                print(u"  WatchDog Timer: \u001b[1mON\u001b[0m")

            i = (data[14] & 0x06) >> 1  # take the 2 bits for LED Indicator

            if (i == 0):
                print(u"  LED Indicator: \u001b[1mOFF\u001b[0m")
            elif (i == 1):
                print(u"  LED Indicator: \u001b[1mON\u001b[0m")
            elif (i == 2):
                print(u"  LED Indicator: \u001b[1mMeasurement\u001b[0m")

            sys.stdout.write(u"  Current Preset Configuration is: ")

            if (data[1] == 0x53):
                print(u"\u001b[1mHigh Speed\u001b[0m")
            elif (data[1] == 0x52):
                print(u"\u001b[1mLong Range\u001b[0m")
            elif (data[1] == 0x41):
                print(u"\u001b[1mHigh Accuracy\u001b[0m")
            elif (data[1] == 0x43):
                print(u"\u001b[1mCustom\u001b[0m")
            elif (data[1] == 0x54):
                print(u"\u001b[1mtinyLiDAR\u001b[0m")
            else:
                print(u"\u001b[1m** UNKNOWN **\u001b[0m")

            sys.stdout.write(u"  Signal Rate Limit = ")
            k = ((data[2]) << 8 | data[3])
            k = k / 65536.0
            print(u"\u001b[1m%.2f MCPS\u001b[0m" % k)

            sys.stdout.write(u"  Sigma Estimate Limit = ")
            print(u"\u001b[1m%d mm\u001b[0m" % data[4])

            sys.stdout.write(u"  Timing Budget = ")
            k = ((data[5]) << 8 | data[6])
            print(u"\u001b[1m%d ms\u001b[0m" % k)

            if (data[7]) == 14:
                print(u"  Pre Range VCSEL Period = \u001b[1m14\u001b[0m ")
                print(u"  Final Range VCSEL Period = \u001b[1m10\u001b[0m ")
            else:
                print(u"  Pre Range VCSEL Period = \u001b[1m18\u001b[0m ")
                print(u"  Final Range VCSEL Period = \u001b[1m14\u001b[0m ")

            sys.stdout.write(u"  tinyLiDAR Firmware Version = ")
            print(u"\u001b[1m" + str(data[8]) + "." + str(data[9]) + "." + str(data[10]) + u"\u001b[0m")

            sys.stdout.write(u"  ST PAL API Version = ")
            print(u"\u001b[1m" + str(data[11]) + "." + str(data[12]) + "." + str(data[13]) + u"\u001b[0m")

            if (data[14] & 0x08):
                print(u"  Offset Cal: \u001b[1mCustom\u001b[0m")
            else:
                print(u"  Offset Cal: \u001b[1mFactory\u001b[0m")

            sys.stdout.write(u"  Cal Offset = ")
            ilong = (data[15] << 24 | data[16] << 16 | data[17] << 8 | data[18]) / 1000.0
            print(u"\u001b[1m%.1f mm\u001b[0m" % ilong)  # for offset only

            sys.stdout.write(u"  Xtalk = ")
            ilong = (data[19] << 24 | data[20] << 16 | data[21] << 8 | data[22]) / 65536.0
            print(u"\u001b[1m%.3f MCPS\u001b[0m" % ilong)

            commandEntered = raw_input(u"\u001b[1B> Press ENTER to Continue ")

            tl.printMenu()
            tl.printMenu1()

            continue

    else:
        print
        '  ** Command Not Valid, please try again **'

print("> closing the I2C port ")
tl.pi.bb_i2c_close(tlv.SDA)
print("> all done! ")

# end of code