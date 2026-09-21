import serial

print("Learning Pyserial")

ser = serial.Serial(port="/dev/ttyACM0", baudrate=19200, timeout=10)

while not ser.is_open:
    print("Opening...")

# TODO: User the ser object


ser.close()
