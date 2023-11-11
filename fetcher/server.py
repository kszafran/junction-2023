import paho.mqtt.client as mqtt


class MotionFrame:
    timestamp: float
    ax: float
    ay: float
    az: float
    ax_g: float
    ay_g: float
    az_g: float
    rot_x: float
    rot_y: float
    rot_z: float
    # heart_rate: float # filled from Google Fit

    def __init__(self, timestamp) -> None:
        self.timestamp = timestamp

    def is_complete(self) -> bool:
        return (
            hasattr(self, "timestamp")
            and hasattr(self, "ax")
            and hasattr(self, "ay")
            and hasattr(self, "az")
            and hasattr(self, "ax_g")
            and hasattr(self, "ay_g")
            and hasattr(self, "az_g")
            and hasattr(self, "rot_x")
            and hasattr(self, "rot_y")
            and hasattr(self, "rot_z")
        )

    def __str__(self) -> str:
        return f"{self.timestamp}: ({self.ax}, {self.ay}, {self.az}) ({self.ax_g}, {self.ay_g}, {self.az_g}) ({self.rot_x}, {self.rot_y}, {self.rot_z})"


cur_frame = None


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")


def on_message(client, userdata, msg):
    global cur_frame
    try:
        attr = topic_to_attr(msg.topic)
        val = float(msg.payload)
        timestamp = int(msg.timestamp)

        # print(f"{timestamp} {attr}={val}")

        if cur_frame is None or hasattr(cur_frame, attr):
            cur_frame = MotionFrame(timestamp)

        cur_frame.__setattr__(attr, val)

        if cur_frame.is_complete():
            next(cur_frame)
            cur_frame = None

    except Exception as e:
        print("Error processing request:", str(e))
        return


def topic_to_attr(topic: str) -> str:
    if topic == "/gyroscope/x":
        return "ax_g"
    if topic == "/gyroscope/y":
        return "ay_g"
    if topic == "/gyroscope/z":
        return "az_g"
    if topic == "/accelerometer/x":
        return "ax"
    if topic == "/accelerometer/y":
        return "ay"
    if topic == "/accelerometer/z":
        return "az"
    if topic == "/magnetometer/x":
        return "rot_x"
    if topic == "/magnetometer/y":
        return "rot_y"
    if topic == "/magnetometer/z":
        return "rot_z"


def next(frame: MotionFrame):
    print(frame)


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()
