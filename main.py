import json
import paho.mqtt.client as mqtt
import time
import os
import string

# Setup client
client = mqtt.Client()
mqtt_IP = os.environ["MQTT_IP"]
client.connect(mqtt_IP, 1883)
client.loop_start()

import hardware
hw_map = {
    "yun1": hardware.Yun1(client),
    "yun3": hardware.Yun3(client)
}

topic_to_handler = {}

for _,klass in hw_map.iteritems():
    topic_to_handler[klass.get_topic() + "/set"] = klass

for topic,_ in topic_to_handler.iteritems():
    client.subscribe(topic)

# Handle messages
def on_message(mosq, obj, msg):
    if msg.topic in topic_to_handler:
        msg_json = json.loads(msg.payload)
        topic_to_handler[msg.topic].handle_sync(msg_json)

client.on_message = on_message

# Loop in main
try:
    while True:
        for name,hw in hw_map.iteritems():
            hw.update()
            print name + "(" + \
                string.join([ k + ": " + str(v) for k, v in hw.get_local_state().iteritems() ], ", ") + \
                ")"

        time.sleep(0.1);

except KeyboardInterrupt:
    print("Shutting down...")
    print("Done!")

client.loop_stop()
