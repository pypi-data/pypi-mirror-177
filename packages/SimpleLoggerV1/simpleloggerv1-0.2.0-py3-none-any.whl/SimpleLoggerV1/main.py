from SimpleLoggerV1 import SimpleLoggerV1

sl = SimpleLoggerV1(method='rtu',serialPort='/dev/ttyACM0')
print(sl.getUid())