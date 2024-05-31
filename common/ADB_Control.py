# import math
import threading
import time
import serial
import serial.tools.list_ports
from typing import Optional
import subprocess as sp
import re

from common import Log_Info

NOT_FOUND_WLAN = 0xFF
SET_PORT_FAIL = 0xFE
SET_WIFI_FAIL = 0xFD
SET_WIFI_OK = 0x00
SET_DISCONNECT_OK = 0x01


class ADBControl:
    def __init__(self, devices_id=None):
        self.__adb_states = False
        self.__ser = None
        self.__wlan_ip = None
        self.__device_id = devices_id
        self.__log = Log_Info.setup_logger('ADB', False)

    @property
    def wlan_ip(self):
        return self.__wlan_ip

    @property
    def adb_states(self):
        """
        标识：用以检测ADB是否使能的标志
        """
        return self.__adb_states

    def fill_ser_list(self, ser_combox):
        """
        功能：将串口信息填充至串口下拉框
        参数1：串口下拉框控件
        """
        temp_list = list()
        ser_list = serial.tools.list_ports.comports()
        for ser_info in ser_list:
            temp_list.append(ser_info.name)
        ser_combox['value'] = temp_list
        if ser_list:
            ser_combox.current(0)

    def __ser_init(self, ser_num: Optional[str], baud: Optional[int]):
        """
        功能：初始化串口对象函数
        参数1：串口号
        参数2：波特率
        """
        try:
            if self.__ser is None:
                self.__ser = serial.Serial(ser_num, baud)
                return True
            else:
                self.__ser.close()
                self.__ser = serial.Serial(ser_num, baud)
                return True
        except (FileNotFoundError, PermissionError):
            return False

    def __send(self, data: Optional[str]):
        """
        通过串口发送数据
        param1：字符串类型数据，需要发送得数据,str
        """
        send_data = "{}\r\n".format(data).encode("UTF-8")
        self.__ser.write(send_data)

    def __enable_adb(self, enable_instruct):
        """
        功能：串口发送使能使能
        参数1：使能指令
        """
        self.__send(enable_instruct)

    def check_adb_connect_thread(self, devices_id, is_wlan=False):
        check_adb_thread = threading.Thread(target=self.__check_adb_is_connect,
                                            args=(devices_id, is_wlan))
        check_adb_thread.start()

    def __check_adb_is_connect(self, devices_id, is_wlan):
        for _ in range(30):  # 循环查询当前设备是否已连接
            time.sleep(0.1)
            is_devices = self.__check_device_states(devices_id)
            if is_devices is True:
                if is_wlan:
                    connect_state = self.adb_wifi_connect(devices_id)
                    if connect_state == NOT_FOUND_WLAN or connect_state == SET_PORT_FAIL or connect_state == SET_WIFI_FAIL:
                        print(connect_state)
                        self.__log.warning("设备与PC不在一个网络下！\n请确定当前设备与PC在同一网络下且有线连接")
                        break
                    elif connect_state == SET_WIFI_OK:
                        self.__device_id = devices_id
                        self.__adb_states = True
                        self.__log.info("当前设备已与PC无线连接，可断开有线使用！")
                        break
                else:
                    self.__device_id = devices_id
                    self.__adb_states = True
                    self.__log.info("有线adb使能成功")
                    break
        else:
            self.__adb_states = False
            self.__log.warning("adb使能失败")

    def check_adb_connect_thread_ser(self, devices_id, enable_instruct, ser_com, baud, is_wlan=False):
        """
        功能：adb使能线程
        参数1：安卓设备id
        参数2：使能指令
        参数3：串口号
        参数4：波特率
        参数5：弹框回调函数
        """
        check_adb_ser_thread = threading.Thread(target=self.__check_adb_is_connect_ser,
                                                args=(devices_id, enable_instruct, ser_com, baud, is_wlan))
        check_adb_ser_thread.start()

    def __check_adb_is_connect_ser(self, devices_id, enable_instruct, ser_com, baud, is_wlan):
        """
        功能：检测adb是否已连接
        参数1：设备id（adb devices可以看到）
        参数2：soc的串口连接的串口号
        """

        init_ser_state = self.__ser_init(ser_com, baud)
        if init_ser_state:
            for _ in range(30):  # 循环查询当前设备是否已连接
                self.__enable_adb(enable_instruct)  # 向串口发送adb_enable指令
                time.sleep(0.1)
                is_devices = self.__check_device_states(devices_id)
                if is_devices is True:
                    if is_wlan:
                        connect_state = self.adb_wifi_connect(devices_id)
                        if connect_state == NOT_FOUND_WLAN or connect_state == SET_PORT_FAIL or connect_state == SET_WIFI_FAIL:
                            self.__log.warning("设备与PC不在一个网络下！\n请确定当前设备与PC在同一网络下且有线连接")
                            break
                        elif connect_state == SET_WIFI_OK:
                            self.__device_id = devices_id
                            self.__adb_states = True
                            self.__log.info("当前设备已与PC无线连接，可断开有线使用！")
                            break
                    else:
                        self.__device_id = devices_id
                        print("self.__device_id", self.__device_id)
                        print("devices_id", devices_id)
                        self.__adb_states = True
                        self.__log.info("有线adb使能成功")
                        break
            else:
                self.__adb_states = False
                self.__log.warning("adb使能失败")
        else:
            self.__log.warning("串口打开失败")

    @staticmethod
    def __check_device_states(devices_id):
        """
        功能：检测设备是否有连接
        参数1：安卓设备id
        """
        try:
            dv_process = sp.Popen('adb devices', stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
        except FileNotFoundError:
            return False
        result_list = dv_process.communicate()
        for rs in result_list:
            result = rs.decode('gbk').strip()
            if result != '':
                if devices_id in result and "offline" not in result:
                    return True
                else:
                    return False

    def adb_screen_crop(self, device_type, path, is_wlan):
        """
        功能：执行截屏命令
        参数1：不同屏幕
        参数2：存放路径
        """
        if is_wlan:
            screen_process = sp.Popen(f"adb -s {self.__wlan_ip} shell screencap -p " + device_type + ' > ' + path,
                                      shell=True)
            screen_process.wait()
        else:
            screen_process = sp.Popen(f"adb -s {self.__device_id} shell screencap -p " + device_type + ' > ' + path,
                                      shell=True)
            screen_process.wait()

    def adb_screen_long_thread(self, device_type, click_x, click_y, press_time, is_wlan=False):
        """
        功能：adb长按指令线程
        参数1：屏幕类型
        参数2：点击x坐标
        参数3：点击y坐标
        参数4：长按时间
        """
        adb_long = threading.Thread(target=self.adb_screen_long_press,
                                    args=(device_type, click_x, click_y, press_time, is_wlan))
        adb_long.start()

    def take_screenshot(self, device_type, path, is_wlan):
        """
        功能：将linux系统下的截图转换为windows系统下的截图
        参数1：截取屏幕类型（上屏还是下屏）
        参数2：需要存储图片的路径
        """
        """adb截取手机屏幕的函数 [path]为存储路径"""
        self.adb_screen_crop(device_type, path, is_wlan)
        """安卓底层是linux,Linux的换行符是\r\n,但是Windows的换行符是\n，所以需要replace替换一下"""
        with open(path, 'rb') as f:
            data = f.read()
        temp_data = data.replace(b'\r\n', b'\n')
        with open(path, 'wb') as f:
            f.write(temp_data)

    def adb_screen_long_press(self, device_type, click_x, click_y, press_time, is_wlan=False):
        """
        功能：adb长按指令
        参数1：屏幕类型
        参数2：点击x坐标
        参数3：点击y坐标
        参数4：长按时间
        """
        if is_wlan:
            sp.run(
                "adb -s {} shell input {} touchscreen swipe {} {} {} {} {}".format(self.__wlan_ip, device_type, click_x,
                                                                                   click_y, click_x, click_y,
                                                                                   press_time))
        else:
            sp.run("adb -s {} shell input {} touchscreen swipe {} {} {} {} {}".format(self.__device_id, device_type,
                                                                                      click_x,
                                                                                      click_y, click_x, click_y,
                                                                                      press_time))

    def adb_screen_click(self, device_type, click_x, click_y, is_wlan=False):
        """
        功能：adb点击指令
        参数1：屏幕类型
        参数2：点击坐标x
        参数3：点击坐标y
        """
        if is_wlan:
            sp.run("adb -s {} shell input {} tap {} {}".format(self.__wlan_ip, device_type, click_x,
                                                               click_y))
        else:
            sp.run("adb -s {} shell input {} tap {} {}".format(self.__device_id, device_type, click_x,
                                                               click_y))

    def adb_screen_swipe(self, device_type, swipe_start_x, swipe_start_y, swipe_stop_x, swipe_stop_y, swipe_time,
                         is_wlan=False):
        """
        功能：adb滑动指令
        参数1：屏幕类型
        参数2：滑动起始坐标x
        参数3：滑动起始坐标y
        参数4：滑动结束坐标x
        参数5：滑动结束坐标y
        """
        # print("滑动")
        # print(swipe_time)
        if is_wlan:
            sp.run("adb -s {} shell input {} touchscreen swipe {} {} {} {} {}".format(self.__wlan_ip, device_type,
                                                                                      swipe_start_x,
                                                                                      swipe_start_y, swipe_stop_x,
                                                                                      swipe_stop_y, swipe_time))
        else:
            sp.run("adb -s {} shell input {} touchscreen swipe {} {} {} {} {}".format(self.__device_id, device_type,
                                                                                      swipe_start_x,
                                                                                      swipe_start_y, swipe_stop_x,
                                                                                      swipe_stop_y, swipe_time))

    def adb_wifi_connect(self, devices_id):
        """
        功能：进行adb的WiFi连接
        参数1：设备id
        """
        wlan_ip = self.get_wlan_info(devices_id)
        if wlan_ip is None:
            return NOT_FOUND_WLAN  # 没有找到热点ip地址
        else:
            self.set_wifi_port(devices_id)
            set_wlan_stare = self.set_wifi_connect(wlan_ip)
            if set_wlan_stare:
                return SET_WIFI_OK  # 设置WiFi连接成功
            else:
                return SET_WIFI_FAIL  # 设置WiFi连接失败

    def get_wlan_info(self, devices_id):
        """
        功能：获取wifi热点ip地址
        参数1：设备id
        """
        get_wlan_process = sp.Popen(f"adb -s {devices_id} shell ifconfig", stdout=sp.PIPE, stdin=sp.PIPE,
                                    stderr=sp.PIPE,
                                    shell=True)
        result_list = get_wlan_process.communicate()
        wlan_data = result_list[0].decode("utf-8")
        get_wlan_process.terminate()
        if re.search('wlan(.+?)Link encap:(.+?)HWaddr([\s\S]+?)inet addr:(.+?)Bcast', wlan_data):
            wlan_info = re.search('wlan(.+?)Link encap(.+?)HWaddr([\s\S]+?)inet addr:(.+?)Bcast', wlan_data).group(4)
            self.__wlan_ip = wlan_info.strip() + ':5555'
            return wlan_info.strip()
        else:
            return None

    def set_wifi_port(self, devices_id):
        """
        功能：设置wifi连接端口
        参数1：设备id
        """
        set_port_process = sp.Popen(f"adb -s {devices_id} tcpip 5555", stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE,
                                    shell=True)
        set_port_process.terminate()

    def set_wifi_connect(self, wlan_ip):
        """
        功能：设置wifi连接
        参数1：wifi热点的ip地址
        """
        set_connect_process = sp.Popen(f"adb connect {wlan_ip}:5555", stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
        result_list = set_connect_process.communicate()
        set_connect_result = result_list[0].decode("utf-8")
        if set_connect_result.strip() == f"connected to {wlan_ip}:5555" or set_connect_result.strip() == f'already connected to {wlan_ip}:5555':
            return True
        else:
            return False

    def close_wifi_connect(self, devices_id):
        """
        功能：断开无线连接
        参数1：设备id
        """
        wlan_ip = self.get_wlan_info(devices_id)
        if wlan_ip is None:
            return NOT_FOUND_WLAN
        else:
            sp.run(f'adb disconnect {wlan_ip}')
            return SET_DISCONNECT_OK


if __name__ == '__main__':
    adb = ADBControl(devices_id="2cdc2011")
    # adb = ADBControl(devices_id="ee87acac")
    # adb = ADBControl()
    # adb.check_adb_connect_thread(devices_id="ee87acac")
    # adb.check_adb_connect_thread_ser(devices_id="ee87acac", enable_instruct="echo 1 > /proc/sys/kernel/printk", ser_com="COM17", baud="115200")
    # adb.take_screenshot(device_type="", path="pic.png", is_wlan=False)
    # adb.adb_screen_crop(device_type="-d 2", path="", is_wlan=False)
    # adb.adb_screen_click(device_type="", click_x=234, click_y=62)
    # adb.adb_screen_long_press(device_type="", click_x=62, click_y=234, press_time=6000)
    # adb.adb_screen_long_press(device_type="", click_x=555, click_y=1870, press_time=20)
    # adb.adb_screen_click(device_type="", click_x=1050, click_y=766)
    # adb.adb_screen_click(device_type="", click_x=62, click_y=234)
    adb.adb_screen_click(device_type="", click_x=800, click_y=2000)

