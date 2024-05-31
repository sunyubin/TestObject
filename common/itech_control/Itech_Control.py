import time
import serial


class ItechControl:
    def __init__(self):
        self.__power_ser = None
        self.address = 0
        self.length_packet = 26

    def init_power(self, ser_com):
        """
        功能：初始化电源配置
        """
        try:
            self.__power_ser = serial.Serial(ser_com, 9600, timeout=1)
            set_remote_state = self.set_remote_control()
            set_on_state = self.turn_out_control()
            if set_remote_state == 0x80 and set_on_state == 0x80:
                return True
            else:
                return False
        except serial.SerialException:
            return False

    def set_remote_control(self, state=False):
        """
        功能：设置为远程控制
        参数1：True:远程控制，False:本地控制
        """
        if state:
            cmd = self.get_command(0x20, 1)
        else:
            cmd = self.get_command(0x20, 1)
        response = self.send_command(cmd)
        return response[3]

    def turn_out_control(self, state=True):
        """
        功能：电源控制
        参数1：True:开启，False:关闭
        """
        if state:
            cmd = self.get_command(0x21, 1)
        else:
            cmd = self.get_command(0x21, 0)
        response = self.send_command(cmd)
        return response[3]

    def set_output_voltage(self, voltage):
        """
        功能：设置当前的电源的电压
        """
        cmd = self.get_command(0x23, 0x1e3 * voltage)
        response = self.send_command(cmd)
        return response[3]

    def set_output_current(self, voltage):
        """
        功能：设置当前的电源的电流
        """
        cmd = self.get_command(0x24, 0x1e3 * voltage)
        response = self.send_command(cmd)
        return response[3]

    def get_voltage_current(self):
        """
        功能:获取输出电压、电流
        """
        query_info = bytearray(
            b'\xaa\x00&\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd0')
        response = self.send_command(query_info)
        current = float(response[4] << 8 | response[3]) / 1000
        voltage = float(response[8] << 24 | response[7] << 16 | response[6] << 8 | response[5]) / 1000
        return current, voltage


    def send_command(self, command):
        """
        功能：向电源串口发送指令并获取返回结果
        参数：需发送的指令，byte数组
        """
        try:
            self.__power_ser.write(command)
            response = self.__power_ser.read(26)

        except serial.SerialException:
            return None
        return response

    def start_command(self, byte):
        """
        功能：协议的头信息
        """
        cmd = bytearray()
        cmd.append(0xaa)  # 协议头
        cmd.append(self.address)  # 电源地址默认是0
        cmd.append(byte)  # 协议密令
        return cmd

    def get_command(self, command, value, num_bytes=4):
        """
        功能：拼接指令
        参数1：
        """
        cmd = self.start_command(command)
        if num_bytes > 0:
            r = num_bytes + 3
            cmd += self.disassembly_data(value)[:num_bytes] + self.add_reserved(r)
        else:
            cmd += self.add_reserved(0)
        cmd.append(self.calculate_checksum(cmd))
        return cmd

    def add_reserved(self, num_used):
        """
        功能：添加空白字节
        参数1：需要填充的空白字节数
        """
        resp = bytearray(self.length_packet - num_used - 1)
        return resp

    def calculate_checksum(self, cmd):
        """
        功能：计算数据的校验值
        参数1：数据
        """
        assert ((len(cmd) == self.length_packet - 1) or (len(cmd) == self.length_packet))
        checksum = 0
        for i in range(self.length_packet - 1):
            checksum += cmd[i]
        checksum %= 256
        return checksum

    def disassembly_data(self, value, num_bytes=4):
        """
        功能：将数据按位进行拆解放置的具体的字节位
        参数1：需要拆解的数据
        参数2：需要放置的字节长度
        """
        assert (num_bytes == 1 or num_bytes == 2 or num_bytes == 4)
        value = int(value)  # Make sure it's an integer
        s = bytearray()
        s.append(value & 0xff)
        if num_bytes >= 2:
            s.append((value & (0xff << 8)) >> 8)
            if num_bytes == 4:
                s.append((value & (0xff << 16)) >> 16)
                s.append((value & (0xff << 24)) >> 24)
                assert (len(s) == 4)
        return s

    def cycle_check_current_thread(self, check_current=0):
        """
        功能：检查电流值的线程
        """

    def cycle_check_current(self, check_current):
        while True:
            current = self.get_voltage_current()
            if current == check_current:
                pass


if __name__ == '__main__':
    power = ItechControl()
    init_state = power.init_power("COM22")
    if init_state:
        # pass
        # # power.set_output_voltage(15)
        a = power.get_voltage_current()
        print(a)
    else:
        print("电源连接成功")


    def get_voltage1(current_base):
        current = 0
        while current_base != current:
            current, voltage = power.get_voltage_current()
            print(current, voltage)
        return True

    print(get_voltage1(2.08))
