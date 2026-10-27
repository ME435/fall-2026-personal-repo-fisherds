import mqtt_helper as mh
import time


def my_callback(message_type, message_payload):
    print("The message type is ", message_type)
    print("The message payload is ", message_payload)

def main():
    print("Hacky MQTT test")
    mqtt_client = mh.MqttClient()
    mqtt_client.connect(subscription_topic_name="fisherds/#",
                        publish_topic_name="fisherds/sending")
    mqtt_client.callback = my_callback

    counter = 0
    while True:
        mqtt_client.send_message("counter", counter)
        time.sleep(2)
        counter += 1


main()
