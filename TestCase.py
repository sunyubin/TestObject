from datetime import datetime
import time
import pytest

from common import Log_Info
from common.ADB_Control import ADBControl
from common.DebugMode import relay_serial
from common.DobotRobot import Dobot
from common.ImgRecognition import ImageRecognizer, ImageCropper
from common.Relay_Serial import RelaySerial
from common.Serial_Control import SerialControl
from common.itech_control.Itech_Control import ItechControl


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


class BT_test:
    def __init__(self):
        self.ser = SerialControl()
        self.recognizer = ImageRecognizer()
        self.adb_phone = ADBControl(devices_id="2cdc2011")
        self.adb_AVN = ADBControl(devices_id="ee87acac")
        self.ser = SerialControl()
        self.ser.ser_init("COM17")
        self.ser.recv_thread()
        self.ser.read_data_thread()
        self.data = ""
        self.Key_ass = False
        self.__log = Log_Info.setup_logger('BTTesting', False)
        self.relay = relay_serial("COM21")
        self.power = ItechControl()
        self.init_state = self.power.init_power("COM22")
        self.test_num = 0

    def is_time_within_range(self, time1_str, time2_str, time_format="%M:%S", allowed_diff=2):
        time1 = datetime.strptime(time1_str, time_format)
        time2 = datetime.strptime(time2_str, time_format)
        # 计算时间差的绝对值
        time_diff = abs((time1 - time2).total_seconds())
        return time_diff <= allowed_diff

    def power_start(self):
        print("power_start ON")
        self.relay.Open_ACC()
        time.sleep(20)
        print(" -su root")
        self.ser.su_root()
        print(" -su root")
        time.sleep(5)
        self.ser.send_data("echo 1 > /proc/sys/kernel/printk")
        print(" -echo 1 > /proc/sys/kernel/printk")
        self.ser.send_data("echo peripheral > /sys/devices/platform/soc/a600000.ssusb/mode")
        print(" -echo peripheral > /sys/devices/platform/soc/a600000.ssusb/mode")
        time.sleep(5)
        self.ser.send_data('logcat | grep -ie "Bad address"')
        print(' -logcat | grep -ie "Bad address"')
        time.sleep(5)
        print("power_start END")

    def power_over(self):
        self.relay.Close_ACC()
        time.sleep(30)
        print("power_over END")
        self.get_voltage(0.04)

    def screenshot_to_text(self):
        phone_config = {
            "music_name": {
                "left": 300,
                "top": 100,
                "right": 800,
                "bottom": 200,
                "save_path": "Img/phone_name.png"
            },
            "music_time": {
                "left": 50,
                "top": 1750,
                "right": 150,
                "bottom": 1820,
                "save_path": "Img/phone_time.png"
            },
            "image_path": "Img/phone_shot.png"
        }
        AVN_config = {
            "music_name": {
                "left": 650,
                "top": 300,
                "right": 1000,
                "bottom": 400,
                "save_path": "Img/AVN_name.png"
            },
            "music_time": {
                "left": 280,
                "top": 640,
                "right": 380,
                "bottom": 700,
                "save_path": "Img/AVN_time.png"
            },
            "image_path": "Img/AVN_shot.png"
        }
        self.adb_AVN.take_screenshot(device_type="-d 0", path=AVN_config["image_path"], is_wlan=False)
        self.adb_phone.take_screenshot(device_type="", path=phone_config["image_path"], is_wlan=False)
        # 截图
        music_time_result = False
        music_name_result = False
        for image_type in ["music_name", "music_time"]:
            AVN_cropper = ImageCropper(AVN_config["image_path"])
            AVN_cropper.crop_and_save(left=AVN_config[image_type]["left"],
                                      top=AVN_config[image_type]["top"],
                                      right=AVN_config[image_type]["right"],
                                      bottom=AVN_config[image_type]["bottom"],
                                      save_path=AVN_config[image_type]["save_path"])
            phone_cropper = ImageCropper(phone_config["image_path"])
            phone_cropper.crop_and_save(left=phone_config[image_type]["left"],
                                        top=phone_config[image_type]["top"],
                                        right=phone_config[image_type]["right"],
                                        bottom=phone_config[image_type]["bottom"],
                                        save_path=phone_config[image_type]["save_path"])
            # 提取
            AVN_text = self.recognizer.RecognizeText(AVN_config[image_type]["save_path"])
            phone_text = self.recognizer.RecognizeText(phone_config[image_type]["save_path"])
            print("Recognized AVN_text:", AVN_text)
            print("Recognized phone_text:", phone_text)
            if image_type == "music_time":
                if self.is_time_within_range(AVN_text, phone_text):
                    music_time_result = True
                else:
                    music_time_result = False
                    break  # 提前退出循环，因为已经确定结果为 False
            elif image_type == "music_name":
                if AVN_text == phone_text:
                    music_name_result = True
                else:
                    music_name_result = False
                    break  # 提前退出循环，因为已经确定结果为 False

        # 检查两个结果变量
        if music_name_result and music_time_result:
            print(f"\033[0;32;40m对比结果一致\033[0m")
            return True
        else:
            print(f"\033[0;31;40m对比结果不一致\033[0m")
            return False

    def get_voltage(self, current_base):
        current = 0
        while current_base != current:
            current, voltage = self.power.get_voltage_current()
        return True

    def Key_assert(self):
        start_time = time.time()
        while time.time() - start_time < 30:
            data = self.ser.read_data()
            if data is not None:
                print(f"{time.time()} -> {data}")
                if "Bad address" in data and "Read header error:" in data:
                    print("Bad_address_YES")
                    self.Key_ass = True

    def click_music_AVN(self):
        self.adb_AVN.adb_screen_long_press(device_type="", click_x=62, click_y=234, press_time=10000)  # 长按menu键
        print("长按menu键")
        self.adb_AVN.adb_screen_click(device_type="", click_x=1050, click_y=766)  # 点击免责声明
        print("点击免责声明")
        self.adb_AVN.adb_screen_click(device_type="", click_x=62, click_y=234)  # 点击menu键
        print("点击menu键")
        self.adb_AVN.adb_screen_click(device_type="", click_x=1125, click_y=387)  # 点击蓝牙音乐
        print("点击蓝牙音乐")

    def click_music_phone(self):
        self.adb_phone.adb_screen_click(device_type="", click_x=555, click_y=2000)  # 点击播放按钮
        print("点击下一曲按钮")

    def Each_round_of_testing(self):
        self.power_over()
        time.sleep(5)
        self.click_music_phone()
        self.power_start()
        time.sleep(10)
        self.click_music_AVN()
        time.sleep(5)
        self.Key_assert()
        time.sleep(5)
        result = self.screenshot_to_text()
        if self.Key_ass is True:
            self.__log.warning(f"第 {self.test_num} 轮，出现Bad_address,无音频播放")
            raise Exception("出现Bad_address,无音频播放")
        elif result is False:
            self.__log.warning(f"第 {self.test_num} 轮，音乐播放页面状态不同步")
            raise Exception("音乐播放页面状态不同步")

    def All_testing(self):
        while self.test_num < 3:
            self.test_num += 1
            self.__log.info(f"第 {self.test_num} 轮测试开始")
            self.Each_round_of_testing()
            self.__log.info(f"第 {self.test_num} 轮测试结束")
            time.sleep(5)


if __name__ == '__main__':
    # a = Robot_test()
    # a.All_testing()
    # time.sleep(10)
    # a.power_start()
    a = BT_test()
    # a.screenshot_to_text()
    a.All_testing()
    # a.Key_assert()
