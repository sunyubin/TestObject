import serial

l = '00 5A 60 01 01 03 00 00 BF'
m = '00 5A 60 01 02 03 00 00 C0'
s = "00 5A 60 01 01 01 00 00 BD"  # R1 ACC-ON
t = "00 5A 60 01 02 01 00 00 BE"

ser = serial.Serial('com12', baudrate=9600)
ser.write(bytes.fromhex(l))
ser.write(bytes.fromhex(s))
ser.close()
