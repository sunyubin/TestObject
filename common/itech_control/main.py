import itech as itech

import time, random


def GetCurrent(power: itech.PowerSupply):
    current = 0
    cmd = power.StartCommand(0x26)
    cmd += power.Reserved(3)
    cmd.append(power.CalculateChecksum(cmd))
    assert (power.CommandProperlyFormed(cmd))
    try:
        response = power.SendCommand(cmd)
    except:
        pass
    if response:
        current = float(response[4] << 8 | response[3]) / 1000
    return current


power = itech.PowerSupply()
power.Initialize('COM16', 9600)
power.SetRemoteControl()
power.TurnOutputOn()

while True:
    startTime = time.time()
    power.SetOutputVoltage(13)
    while GetCurrent(power) < 2.2:
        time.sleep(1)
        print(time.time() - startTime)
        if time.time() - startTime > 30:
            print(f'startup error {time.time() - startTime} s and {GetCurrent(power)} A')
            startTime = time.time()
        pass

    print(f'start up time {time.time() - startTime} s and {GetCurrent(power)} A')
    while time.time() - startTime < 30 or GetCurrent(power) < 2.2:
        pass
    l = random.randint(1, 1)

    try:
        for i in range(l):
            v = random.uniform(1.7, 2.5)
            t = random.uniform(0.05, 1)
            print(f'{i}: Voltage:{v} hold {t} s')
            power.SetOutputVoltage(v)
            time.sleep(random.uniform(0.05, 1))
            power.SetOutputVoltage(13)
            time.sleep(random.uniform(0.05, 1))
            power.SetOutputVoltage(3.99)
            time.sleep(random.uniform(0.05, 1))
    except:
        pass

'''    
    #time.sleep(30)
    power.SetOutputVoltage(1.8)
    time.sleep(15)
    power.SetOutputVoltage(11.8)
    time.sleep(0.0001)
    power.SetOutputVoltage(1.8)
    time.sleep(0.0005)
    power.SetOutputVoltage(-3.96)
    time.sleep(0.0001)
    power.SetOutputVoltage(6.8)
    time.sleep(0.0001)
    power.SetOutputVoltage(-0.5)
    time.sleep(0.0001)
    power.SetOutputVoltage(4.1)
    time.sleep(0.0001)
    power.SetOutputVoltage(0.4)
    time.sleep(0.0001)
    power.SetOutputVoltage(3)
    time.sleep(0.0001)
    power.SetOutputVoltage(1.8)
    time.sleep(0.001)
    power.SetOutputVoltage(13.8)
    time.sleep(0.0001)
    power.SetOutputVoltage(5.2)
    time.sleep(0.0005)
    power.SetOutputVoltage(10)
    time.sleep(0.0005)
'''

# state = power.GetIntegerFromLoad(0x26, msg="Get Power state", num_bytes=22)
# ower.TurnOutputOff()p
power.sp.close()

# load = itech.DCLoad()
# load.Initialize('COM5', 9600)
# load.EnableLocalControl()
# load.SetRemoteControl()
# load.TurnLoadOn()
#
# Current = load.GetIntegerFromLoad(0x26, msg="Get Power state", num_bytes=4)
# print(Current)
# load.TurnLoadOff()
# time.sleep(2)
