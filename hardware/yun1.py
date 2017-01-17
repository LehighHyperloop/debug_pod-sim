import json
import string
import time

class Yun1():
    _name = "arduino-yun1"
    _client = None

    def __init__(self, client):
        self._client = client

    def get_topic(self):
        return "remote/" + self._name

    # Internal State
    _local_state = {
        "relays": [False, False, False, False, False, False, False, False]
    }

    # Serialization
    def serialize_state(self, state):
        return {
            "relays": string.join([ "1" if v else "0" for v in state["relays"]], "")
        }

    def deserialize_state(self, serialized):
        state = {}
        if "relays" in serialized:
            state["relays"] = []
            for v in serialized["relays"]:
                state["relays"].append((v == "1"))

        return state

    def get_local_state(self):
        return self.serialize_state(self._local_state)

    # Communication
    def send_status_update(self):
        self._client.publish(self.get_topic(),
                json.dumps(self.get_local_state()))

    def handle_sync(self, msg_json):
        self._last_update = time.time()
        self._local_state = self.deserialize_state(msg_json)

        self.send_status_update()
