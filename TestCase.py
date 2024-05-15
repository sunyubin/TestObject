import datetime
import time

import pytest
from common.DobotRobot import Dobot
from common.Serial_Control import SerialControl


@pytest.mark.repeat(5)
def Atest_Color():
    print("Testing Color")


def Atest_Robot():
    print("start Testing Robot")
    ser = SerialControl()
    ser.ser_init("COM14")
    ser.recv_thread()
    ser.read_data_thread()
    homeX, homeY, homeZ = 250, 0, 50

    ctrlBot = Dobot(homeX, homeY, homeZ)  # Create DoBot Class Object with home position x,y,z
    ctrlBot.moveHome()
    print("moveArmXY(250, 100)")
    # ctrlBot.moveArmXY(250, 100)
    ctrlBot.moveArmXY(250, 0)

    timer = 0
    while True:
        timer += 1
        print(f"第{timer}次测试")
        print("pickToggle(-40)")
        ctrlBot.pickToggle(-40)
        time.sleep(3)
        # print("moveHome()")
        # ctrlBot.moveHome()
        data = ser.read_data()
        if data is not None:
            ser.queue_clear()
            print("queue_clear")
            print(data)
            if "BTN_TOUCH" in data:
                print("BTN_TOUCH Yes")


if __name__ == '__main__':
    Atest_Robot()
