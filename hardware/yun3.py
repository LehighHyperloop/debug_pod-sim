from .hardware import Hardware
import json
import random
import string

class Yun3(Hardware):
    _name = "arduino-yun3"
    _local_state = {
        "x": random.random() * 0.2,
        "y": random.random() * 0.2,
        "z": random.random() * 0.2,
    }

    def serialize_state(self, state):
        return self._local_state

    def update(self):
        self._local_state = {
            "x": random.random() * 0.2,
            "y": random.random() * 0.2,
            "z": random.random() * 0.2,
        }
        self._client.publish("sensor/center/accel", json.dumps(self._local_state))
