import serial
import time

class PlateLoader:
    def __init__(self):
        self.is_connected = False
        self.ser = None

    def connect(self, port="/dev/cu.usbmodem11301"):
        if self.is_connected:
            return  # Prevent multiple connections
        
        self.ser = serial.Serial(port, baudrate=19200, timeout=1)  # Use a timeout to prevent blocking
        self.is_connected = True
        print("Connecting... Connected!")  # No need to check ser.is_open

        time.sleep(1)  # Allow time for device to initialize
        self.ser.reset_input_buffer()

    def send_command(self, command):
        if not self.is_connected:
            self.connect()

        # Sending
        message_bytes = (command + "\n").encode()
        print("Sending:", message_bytes)
        self.ser.write(message_bytes)

        # Receiving
        response = b""
        while self.ser.in_waiting == 0:
            time.sleep(0.1)

        while self.ser.in_waiting > 0:
            response = self.ser.readline()
            print("Received:", response.decode().strip())

        return response.decode().strip()

    def disconnect(self):
        if self.is_connected and self.ser:
            self.ser.close()
            self.is_connected = False
            print("Disconnected.")

if __name__ == "__main__":
    print("Testing PlateLoader")
    plateloader = PlateLoader()
    plateloader.connect("/dev/ttyACM0")
    try:
        while True:
            print("\n\n0. Exit")
            print("1. RESET")
            print("2. X-AXIS")
            selection = input("Make a selection: ")

            if selection == "0":
                break
            elif selection == "1":
                response = plateloader.send_command("RESET")
            elif selection == "2":
                to_where = input("Enter X-AXIS position: ")
                response = plateloader.send_command(f"X-AXIS {to_where}")
            else:
                print("Invalid selection", selection)
                continue
            
            print("Response:", response)
    finally:
        plateloader.disconnect()  # Ensure cleanup
        print("Goodbye!")


