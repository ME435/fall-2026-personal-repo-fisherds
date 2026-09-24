import serial
import time

class PlateLoader:
    def __init__(self, port="/dev/ttyACM0"):
        self.port = port
        self.ser = None

    def connect(self):
        if self.ser and self.ser.is_open:
            return
        self.ser = serial.Serial(self.port, baudrate=19200, timeout=15.0)
        time.sleep(2.0)  # Arduino resets when the port opens
        self.ser.reset_input_buffer()
        print(f"Connected to {self.port}")

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Disconnected.")

    def send_command(self, command):
        if not self.ser or not self.ser.is_open:
            self.connect()

        # Sending
        self.ser.reset_input_buffer()
        message_bytes = (command + "\n").encode()
        print("Sending:", message_bytes)
        self.ser.write(message_bytes)

        # Receiving
        response_bytes = self.ser.readline()
        if not response_bytes:
            print(f"Timeout: no response to {command}")
            return "TIMEOUT"
        response = response_bytes.decode().strip()
        print(f"Received: {response}")

        return response
