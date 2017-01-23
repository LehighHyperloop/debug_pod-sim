from .hardware import Hardware

class Yun1(Hardware):
    _name = "arduino-yun1"

    # Internal State
    _local_state = {
        "t": "",
        "relays": [False, False, False, False, False, False, False, False]
    }

    # Serialization
    def serialize_state(self, state):
        return {
            "t": state["t"],
            "relays": "".join([ "1" if v else "0" for v in state["relays"]])
        }

    def deserialize_state(self, serialized):
        state = {}

        if "t" in serialized:
            state["t"] = serialized["t"]

        if "relays" in serialized:
            state["relays"] = []
            for v in serialized["relays"]:
                state["relays"].append((v == "1"))

        return state

