import json

class Hardware:
    _client = None
    _local_state = None

    def __init__(self, client):
        self._client = client

    def get_topic(self):
        return "remote/" + self._name

    def get_local_state(self):
        return self.serialize_state(self._local_state)

    def update(self):
        pass

    # Communication
    def send_status_update(self):
        self._client.publish(self.get_topic(),
                json.dumps(self.get_local_state()))

    def handle_sync(self, msg_json):
        self._local_state = self.deserialize_state(msg_json)
        self.send_status_update()

