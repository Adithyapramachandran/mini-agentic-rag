import json
import time

def save_trace(trace):

    filename = (
        f"logs/{int(time.time())}.json"
    )

    with open(
        filename,
        "w"
    ) as f:

        json.dump(
            trace,
            f,
            indent=2
        )