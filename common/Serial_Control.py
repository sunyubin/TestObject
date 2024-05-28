import threading
import time

import eventlet
import serial
from typing import Optional
from common import Log_Info
import queue


class SerialControl:
    def __init__(self):
        self.__ser = None
        self.__recv_flag = True
        self.__ser_log = Log_Info.setup_logger('Serial', False)
        self.__recv_queue = queue.Queue()
        self.__ser_data = ''
        self.data = ''

    def stop_check(self):
        """
        功能：停止检测
        """
        self.__recv_flag = False

    def ser_init(self, ser_num: Optional[str]):
        """初始化串口对象函数"""
        try:
            self.__ser = serial.Serial(ser_num, 115200)
            return True
        except serial.serialutil.SerialException:
            return False

    def send_data(self, data: Optional[str]):
        """
        功能：重启设备
        """
        self.__send(data)

    # def get_memory_log_thread(self):
    #     """
    #     功能：记录串口log线程
    #     """
    #     record_thread = threading.Thread(target=self.get_memory_log)
    #     record_thread.start()
    #
    # def get_memory_log(self):
    #     """
    #     功能：获取内存日志信息
    #     """
    #     instruct = 'cat /proc/meminfo'
    #     while self.__recv_flag:
    #         self.send_data(instruct)
    #         time.sleep(60)

    def recv_thread(self):
        """
        开启接收线程
        :return:
        """
        recv_td = threading.Thread(target=self.__recv_data)
        recv_td.daemon = True
        recv_td.start()

    def __recv_data(self):
        recv_data = b''
        self.__ser.flushInput()
        while self.__recv_flag:
            try:
                # print(self.__ser.read(1))
                if self.__ser.inWaiting() > 0:
                    recv_text = (self.__ser.read(self.__ser.inWaiting()))
                    recv_data += recv_text
                else:
                    if recv_data != b"":
                        log_info = recv_data.decode('utf-8', errors='ignore')
                        if self.__recv_queue.full() is False:
                            self.__recv_queue.put(log_info)
                        self.__ser_log.info(log_info + '\n')
                        recv_data = b''
                time.sleep(0.001)
            except serial.serialutil.SerialException:
                self.__ser_log.warning("串口断连")
                self.__recv_flag = False

    def __send(self, sd_data: Optional[str]):
        """
        通过串口发送数据
        param1：字符串类型数据，需要发送得数据,str
        """
        send_data = "{}\r\n".format(sd_data).encode("gbk")
        self.__ser.write(send_data)

    def __get_data(self):
        while True:
            data = self.__recv_queue.get()
            self.__ser_data += data

    def read_data_thread(self):
        get_data_td = threading.Thread(target=self.__get_data)
        get_data_td.daemon = True
        get_data_td.start()

    def read_data(self):
        if self.__ser_data != "":
            ser_data = self.__ser_data
            self.__ser_data = ""
            return ser_data

    def queue_clear(self):
        self.__recv_queue.queue.clear()

    def su_root(self, password="HSAE2hmct!!"):
        su_root = False
        while su_root is False:
            self.send_data("su")
            while su_root is False:
                data = self.read_data()
                if data is not None:
                    print("data", data)
                    if "enter password:" in data or "try agian:" in data:
                        self.send_data(password)
                        while su_root is False:
                            data = self.read_data()
                            if data is not None and "console:/ #" in data:
                                su_root = True
                                return True
            time.sleep(0.5)
        time.sleep(0.5)


if __name__ == '__main__':
    ser = SerialControl()
    result = ser.ser_init("COM9")
    print(result)
    ser.recv_thread()
    ser.read_data_thread()
    result = ser.su_root()
    print(result)
    # ser.send_data("su")
    # time.sleep(2)
    # ser.send_data("HSAE2hmct!!")

    # data = ser.read_data()
    # a = ser.su_root()
    # print(a)
    # su_root = False
    # while su_root is False:
    #     print(su_root)
    #     su_root = ser.su_root()
    #     print(su_root)

    # print(" -Key_assert")
    # # Key_ass = False
    # ser.read_data_thread()
    # # while self.Key_assert is True:
    # for i in range(10):
    #     flag_time = 0
    #     ser.queue_clear()
    #     # self.Clck_Home()
    #     while flag_time < 20:
    #         data = ser.read_data()
    #         if data is None:
    #             flag_time += 1
    #         elif data is not None:
    #             print(data)
    #             if "BTN_TOUCH" in data:
    #                 print("BTN_TOUCH_YES")
    #         time.sleep(0.1)
    # su_root = False
    # print(" -su root")
    # while su_root is False:
    #     print("su_root", su_root)
    #     ser.send_data("su")
    #     while su_root is False:
    #         data = ser.read_data()
    #         if data is not None:
    #             print("1", data)
    #             if "enter password:" in data or "try agian:" in data:
    #                 ser.send_data("HSAE2hmct!!")
    #                 while True:
    #                     data = ser.read_data()
    #                     if data is not None:
    #                         if "console:/ #" in data:
    #                             su_root = True
