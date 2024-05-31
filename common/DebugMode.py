import serial

l = '00 5A 60 01 01 03 00 00 BF'
m = '00 5A 60 01 02 03 00 00 C0'
s = "00 5A 60 01 01 01 00 00 BD"  # R1 ACC-ON
t = "00 5A 60 01 02 01 00 00 BE"


class relay_serial:
    def __init__(self, ser_num):
        self.ser = serial.Serial(ser_num, baudrate=9600)

    def Open_ACC(self):
        self.ser.write(bytes.fromhex(s))

    def Open_B(self):
        self.ser.write(bytes.fromhex(l))

    def Close_ACC(self):
        self.ser.write(bytes.fromhex(t))

    def Close_B(self):
        self.ser.write(bytes.fromhex(m))

    def Close_relay(self):
        self.ser.close()


a = relay_serial("com21")
# a.Close_ACC()
# a.Close_B()
# a.Open_ACC()
# a.Open_B()
a.Close_relay()