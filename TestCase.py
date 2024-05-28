import datetime
import time
import eventlet  # 导入eventlet这个模块
import pytest

from common import Log_Info
from common.DobotRobot import Dobot
from common.Relay_Serial import RelaySerial
from common.Serial_Control import SerialControl


@pytest.mark.repeat(5)
def Atest_Color():
    print("Testing Color")


class Robot_test:
    def __init__(self):
        self.ser = SerialControl()
        self.ser.ser_init("COM9")
        self.ser.recv_thread()
        self.ser.read_data_thread()
        homeX, homeY, homeZ = 250, 0, 50
        self.ctrlBot = Dobot(homeX, homeY, homeZ)
        self.data = ""
        self.Key_ass = True
        self.__log = Log_Info.setup_logger('RobotTesting', False)
        self.relay = RelaySerial("COM8")
        self.test_num = 0


    def Equipment_start(self):
        self.ser.recv_thread()
        self.ser.read_data_thread()
        self.ctrlBot.moveHome()

    def power_start(self):
        print("power_start ON")
        self.relay.switch_B(1)
        time.sleep(1)
        self.relay.switch_B(1)
        time.sleep(20)
        print(" -su root")
        self.ser.su_root()
        print(" -su root")
        time.sleep(5)
        self.ser.send_data("echo 1 > /proc/sys/kernel/printk")
        self.ser.send_data("echo 1 > /proc/sys/kernel/printk")
        print(" -echo 1 > /proc/sys/kernel/printk")
        time.sleep(5)
        self.ser.send_data("getevent -lt /dev/input/event2")
        self.ser.send_data("getevent -lt /dev/input/event2")
        print(" -getevent -lt /dev/input/event2")
        time.sleep(5)
        print("power_start END")

    def power_over(self):
        self.relay.switch_B(0)
        time.sleep(10)
        print("power_over END")

    def Clck_Home(self):
        print(" -开始点击移动HOME按键")
        print(" -self.ctrlBot.moveArmXY(180, -133), 移动HOME按键")
        self.ctrlBot.moveArmXY(180, -133)
        print(" -pickToggle(-24)")
        self.ctrlBot.pickToggle(-25)
        self.ctrlBot.pickToggle(-25)

    def Clck_Menu(self):
        print(" -开始点击移动MENU按键")
        print(" -self.ctrlBot.moveArmXY(200, -132), 移动MENU按键")
        self.ctrlBot.moveArmXY(200, -132)
        print(" -pickToggle(-24)")
        self.ctrlBot.pickToggle(-25)
        self.ctrlBot.pickToggle(-25)

    def Key_assert(self):
        flag_time = 0
        while flag_time < 30:
            data = self.ser.read_data()
            if data is None:
                flag_time += 1
            elif data is not None:
                print(data)
                if "BTN_TOUCH" in data or "EV_ABS" in data or "EV_SYN" in data or "EV_KEY" in data:
                    print("BTN_TOUCH_YES")
                    self.Key_ass = True

    def Clck_Home_assert(self):
        self.Key_ass = False
        self.Clck_Home()
        self.Key_assert()
        if self.Key_ass is False:
            self.__log.warning("点击 Home 时没有抓到报文")
            raise Exception("点击 Home 时没有抓到报文")

    def Clck_Menu_assert(self):
        self.Key_ass = False
        self.Clck_Menu()
        self.Key_assert()
        if self.Key_ass is False:
            self.__log.warning("点击 Menu 时没有抓到报文")
            raise Exception("点击 Menu 时没有抓到报文")

    def Each_round_of_testing(self):
        for i in range(1, 501):
            # print(f"第 {i} 小轮点击测试开始")
            self.__log.info(f" 第 {i} 小轮点击测试开始")
            self.Clck_Home_assert()
            time.sleep(10)
            # time.sleep(3)
            self.Clck_Menu_assert()
            time.sleep(10)
            # time.sleep(3)
            # print(f"第 {i} 小轮点击测试结束")
            self.test_num += 1
            print(f"\033[0;31;40m已执行 {self.test_num} 轮测试\033[0m")
            self.__log.info(f"      已执行 {self.test_num} 轮测试     ")

    def All_testing(self):
        # self.Equipment_start()
        for i in range(1, 51):
            print(f"第 {i} 大轮测试开始")
            self.power_over()
            time.sleep(5)
            self.__log.info(f"第 {i} 大轮测试开始")
            self.power_start()
            time.sleep(20)
            self.Each_round_of_testing()
            time.sleep(20)
            print(f"第 {i} 大轮测试结束")
            self.__log.info(f"第 {i} 大轮测试结束")


if __name__ == '__main__':
    a = Robot_test()
    a.All_testing()
    # time.sleep(10)
    # a.power_start()