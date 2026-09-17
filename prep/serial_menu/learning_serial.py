import serial
import time

def main():
    ser = serial.Serial("/dev/ttyACM0", baudrate=19200, timeout=5)
    time.sleep(2)
    ser.reset_input_buffer()
    message_bytes = "GRIPPER OPEN\n".encode()

    print("Sending:", message_bytes)
    ser.write(message_bytes)
    sent_time = time.time()

    response_bytes = ser.readline()
    receive_time = time.time()
    print("Received:", response_bytes)
    print("Message time", receive_time - sent_time, "seconds")



main()