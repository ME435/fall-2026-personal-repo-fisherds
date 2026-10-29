import gpiozero as gz
import mqtt_helper as mh
import signal
import time

class App:

    def __init__(self):
        self.red_led = gz.LED(14)
        self.yellow_led = gz.LED(15)
        self.green_led = gz.LED(18)

        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="me435/fisherds/#",
                                 publish_topic_name="me435/fisherds/to_computer")
        self.mqtt_client.callback = self.mqtt_callback

        self.button23 = gz.Button(23)
        self.button23.when_pressed = lambda : self.mqtt_client.send_message("button")
        self.button25 = gz.Button(25)
        self.button25.when_pressed = lambda : self.mqtt_client.send_message("reset")

    def mqtt_callback(self, message_type, message_payload):
        print("Received type: ", message_type)
        print("Received payload: ", message_payload)

        if message_type == "red":
            if message_payload == "on":
                self.red_led.on()
            elif message_payload == "off":
                self.red_led.off()

        if message_type == "yellow":
            if message_payload == 1:
                self.yellow_led.on()
            elif message_payload == 0:
                self.yellow_led.off()

        if message_type == "green":
            if message_payload:
                self.green_led.on()
            else:
                self.green_led.off()

        if message_type == "leds":
            if message_payload[0] == 1:
                self.red_led.on()
            else:
                self.red_led.off()

            if message_payload[1] == 1:
                self.yellow_led.on()
            else:
                self.yellow_led.off()

            if message_payload[2] == 1:
                self.green_led.on()
            else:
                self.green_led.off()


def main():
    print("GPIO MQTT")
    app = App()

    # while True:
    #     # Send test messages!
    #     # app.mqtt_client.send_message("red", "on")
    #     # app.mqtt_client.send_message("yellow", 1)
    #     # app.mqtt_client.send_message("green", True)
    #     app.mqtt_client.send_message("leds", [1, 0, 1])
    #     time.sleep(1)
    #     # app.mqtt_client.send_message("red", "off")
    #     # app.mqtt_client.send_message("yellow", 0)
    #     # app.mqtt_client.send_message("green", False)
    #     app.mqtt_client.send_message("leds", [0, 1, 0])
    #     time.sleep(1)
    
    signal.pause() # Keep the program alive but does nothing.

main()
