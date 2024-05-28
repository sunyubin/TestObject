import re
import threading
import serial
import time
from typing import Optional
from queue import Queue
# from openpyxl import Workbook,load_workbook


class RelaySerial():
    def __init__(self, port: Optional[str], bps: Optional[int] = 9600, is_query=0):
        self.states_list = []
        self.__read_q = Queue(10)
        self.__ser = None
        self.__recv_flag = True
        self.__is_query = is_query
        self.ser_init(port, bps)

    def ser_init(self, port: Optional[str], bps: Optional[int]):
        """初始化串口对象函数"""
        try:
            self.__ser = serial.Serial(port, bps)
            if self.__is_query == 1:
                self.recv_start_time_thread()
            elif self.__is_query == 2:
                self.recv_mode_switch_thread()
            return self.__ser
        except Exception as e:
            print(e)
            return self.__ser

    @property
    def ser_state(self):
        """返回当前串口状态"""
        return self.__ser.isOpen()

    def flushInput(self):
        """清空输入缓存区"""
        self.__ser.flushInput()

    def flushOutput(self):
        """清空输出缓存区"""
        self.__ser.flushOutput()

    def open(self):
        """开启串口"""
        if self.__ser != None:
            if self.__ser.isOpen() == False:
                self.__ser.open()
                if self.__is_query == 1:
                    self.recv_start_time_thread()
                elif self.__is_query == 2:
                    self.recv_mode_switch_thread()

    def close(self):
        """关闭串口"""
        if self.__ser != None:
            if self.__ser.isOpen() == True:
                self.__ser.close()
                if self.__is_query:
                    self.__recv_flag = False

    def delay_state_query(self):
        if self.__is_query:
            query_state = 'FF'
            self.__send(query_state)
            data = self.__read_q.get()
            return data
        else:
            return None

    def delay_control(self, mode):
        print(1234)
        power_open = 'A0 01 01 A2'
        power_close = 'A0 01 00 A1'
        acc_open = 'A0 02 01 A3'
        acc_close = 'A0 02 00 A2'
        ign_open = 'A0 03 01 A4'
        ign_close = 'A0 03 00 A3'
        if mode == 1:
            self.__send(power_open)
        elif mode == 2:
            self.__send(power_close)
        elif mode == 3:
            self.__send(acc_open)
        elif mode == 4:
            self.__send(acc_close)
        elif mode == 5:
            self.__send(ign_open)
        elif mode == 6:
            self.__send(ign_close)
        elif mode == 7:
            self.__send(power_open)
            self.__send(acc_open)
            self.__send(ign_open)
        elif mode == 8:
            self.__send(power_close)
            self.__send(acc_close)
            self.__send(ign_close)

    def __send(self, data: Optional[str]):
        """
        通过串口发送数据
        param1：字符串类型数据，需要发送得数据,str
        """
        send_data = bytes.fromhex(data)
        self.__ser.write(send_data)

    def recv_start_time(self):
        """
        通过串口检测接受到得数据
        param1：需要检测得数据,str
        param2：循环检测次数,int
        param3：循环检查时间间隔,float
        """
        data = ''
        while self.__recv_flag:  # 超时函数1.5s
            if self.__ser.inWaiting() > 0:
                print("1122345")
                r_text = (self.__ser.read(self.__ser.inWaiting()))
                data += (r_text.decode("utf-8")).strip()  # 持续接收数据
            else:
                if data != '':
                    self.__read_q.put(data)
                    data = ''
            time.sleep(0.05)

    def recv_mode_switch(self):
        data = ''
        temp_data = ''
        num = 0
        while self.__recv_flag:  # 超时函数1.5s
            if self.__ser.inWaiting() > 0:
                r_text = (self.__ser.read(self.__ser.inWaiting()))
                data += (r_text.decode("utf-8",errors='ignore')).strip()  # 持续接收数据
                num = 0
            else:
                if data.strip() != "":
                    temp_data += data
                    data = ''
            time.sleep(0.1)
            num += 1
            if num == 100:
                print("----")
                print(temp_data)
                print("----")
                self.analysis_data(temp_data)
                break




    def analysis_data(self,data,is_sleep =False):
        if is_sleep:
            idle_state = data.split('] SystemState in idle')[0].split('[')[-1]
            idle_data = str(int(idle_state.strip('0'))/1000)
            wake_up_state = data.split('] SystemState in wakeup')[0].split('[')[-1]
            wake_up_data = str(int(wake_up_state.strip('0'))/1000)
            ready_state = data.split('] SystemState in ready')[0].split('[')[-1]
            ready_data = str(int(ready_state.strip('0'))/1000)
            open_state = data.split('] SystemState in open')[0].split('[')[-1]
            open_data = str(int(open_state.strip('0'))/1000)
            normal_state = data.split('] SystemState in normal')[0].split('[')[-1]
            normal_data = str(int(normal_state.strip('0'))/1000)
            sleep_data = data.split('] SystemState in sleep')[0].split('[')[-1]
            self.states_list=[idle_data,wake_up_data,ready_data,open_data,normal_data,sleep_data]
        else:
            wake_up_state = data.split('] SystemState in wakeup')[0].split('[')[-1]
            print(wake_up_state)
            wake_up_data = str(int(wake_up_state) / 1000)
            ready_state = data.split('] SystemState in ready')[0].split('[')[-1]
            ready_data = str(int(ready_state) / 1000)
            open_state = data.split('] SystemState in open')[0].split('[')[-1]
            open_data = str(int(open_state) / 1000)
            normal_state = data.split('] SystemState in normal')[0].split('[')[-1]
            normal_data = str(int(normal_state) / 1000)
            sleep_state = data.split('] SystemState in sleep')[0].split('[')[-1]
            sleep_data = str(int(sleep_state) / 1000)
            self.states_list = [wake_up_data, ready_data, open_data, normal_data, sleep_data]

    def switch_B(self, mode):
        # new
        B_open = 'A0 04 01 A5'
        B_close = 'A0 04 00 A4'
        if mode == 1:
            self.__send(B_open)
            print("Switch B open")
        elif mode == 0:
            self.__send(B_close)
            print("Switch B close")

    # @staticmethod
    # def write_dara(data_list):
    #     wb = load_workbook(r"C:\Users\Administrator\Desktop\检测报告.xlsx")
    #     ws = wb["电控时序时间检测"]
    #     ws.cell(row=1, column=1).value = "idle状态机上电耗时"
    #     ws.cell(row=1, column=2).value = "wake_up状态机上电耗时"
    #     ws.cell(row=1, column=3).value = "ready状态机上电耗时"
    #     ws.cell(row=1, column=4).value = "open状态机上电耗时"
    #     ws.cell(row=1, column=5).value = "normal状态机上电耗时"
    #     for num in range(len(data_list)):
    #         ws.cell(row=2 + num, column=1).value = data_list[num][0]
    #         ws.cell(row=2 + num, column=2).value = data_list[num][1]
    #         ws.cell(row=2 + num, column=3).value = data_list[num][2]
    #         ws.cell(row=2 + num, column=4).value = data_list[num][3]
    #         ws.cell(row=2 + num, column=5).value = data_list[num][4]
    #     wb.save(r"C:\Users\Administrator\Desktop\检测报告.xlsx")
    #
    # @staticmethod
    # def write_sleep_dara(data_list):
    #     wb = load_workbook(r"C:\Users\Administrator\Desktop\检测报告.xlsx")
    #     ws = wb['休眠耗时']
    #     ws.cell(row=1, column=1).value = "ready状态机上电耗时"
    #     ws.cell(row=1, column=2).value = "open状态机上电耗时"
    #     ws.cell(row=1, column=3).value = "normal状态机上电耗时"
    #     ws.cell(row=1, column=4).value = "sleep状态机下电耗时"
    #     for num in range(len(data_list)):
    #         ws.cell(row=2 + num, column=1).value = str(float(data_list[num][1])-float(data_list[num][0]))
    #         ws.cell(row=2 + num, column=2).value = str(float(data_list[num][2])-float(data_list[num][1]))
    #         ws.cell(row=2 + num, column=3).value = str(float(data_list[num][3])-float(data_list[num][2]))
    #         ws.cell(row=2 + num, column=4).value = str(float(data_list[num][4])-float(data_list[num][3]))
    #     wb.save(r"C:\Users\Administrator\Desktop\检测报告.xlsx")



    def recv_mode_switch_thread(self):
        recv_t1 = threading.Thread(target=self.recv_mode_switch)
        recv_t1.start()

    def recv_start_time_thread(self):
        recv_t = threading.Thread(target=self.recv_start_time)
        recv_t.start()



if __name__ == '__main__':
    relay = RelaySerial("COM8")
    relay.switch_B(1)
    # relay.delay_control(1)
    # time.sleep(5)
    # relay.delay_control(3)
    # time.sleep(5)
    # relay.delay_control(5)
    # relay.delay_control(5)

