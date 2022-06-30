class Controller:
    def __init__(self, events: list):
        self.active_tab = None
        self.feed_rate_set = None
        self.stepsize_set = None
        self.x_coord_set = None
        self.y_coord_set = None
        self.z_coord_set = None

        self.door_height = None
        self.door_width = None
        self.door_d = None
        self.door_k = None
        self.door_hinge_path = None
        self.door_width_path = None

        self.x = 0
        self.y = 0
        self.z = 0
        self.abs_x = 0
        self.abs_y = 0
        self.abs_z = 0
        self.wco_x = 0
        self.wco_y = 0
        self.wco_z = 0
        self.status = None

        self.scheduler = []

        self.events = {event: dict() for event in events}

    def get_subscribers(self, event: str):
        return self.events[event]

    def subscribe(self, event: str, observer, callback):
        self.get_subscribers(event)[observer] = callback

    def unsubscribe(self, event: str, observer):
        del self.get_subscribers(event)[observer]

    def dispatch(self, event: str, *args, **kwargs):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(*args, **kwargs)

    def decode_status(self, string: str) -> None:
        string = string.decode("utf-8")
        if string.find("<") == 0:
            try:
                self.status = string[string.index("<") + 1 : string.index("|")]
            except Exception as e:
                print(e)
        if string.find("MPos:") != -1:
            try:
                mpos = string[
                    string.find("MPos:") + len("MPos:") : string.find("|FS:")
                ].split(",")
            except Exception as e:
                print(e)
            try:
                self.abs_x = float(mpos[0])
                self.abs_y = float(mpos[1])
                self.abs_z = float(mpos[2])
            except Exception as e:
                print(e)

        if string.find("WCO:") != -1:
            try:
                wco = string[string.find("WCO:") + len("WCO:") : -3].split(",")
            except Exception as e:
                print(e)
            try:
                self.wco_x = float(wco[0])
                self.wco_y = float(wco[1])
                self.wco_z = float(wco[2])
            except Exception as e:
                print(e)

        if self.status == "Idle":
            self.dispatch(event="machine_free")
        else:
            self.dispatch(event="machine_busy")

        self.x = round(self.abs_x - self.wco_x, 3)
        self.y = round(self.abs_y - self.wco_y, 3)
        self.z = round(self.abs_z - self.wco_z, 3)

        self.dispatch(
            event="new_coord",
            x_coord=self.x,
            y_coord=self.y,
            z_coord=self.z,
            x_abs=self.abs_x,
            y_abs=self.abs_y,
            z_abs=self.abs_z,
            wco_x=self.wco_x,
            wco_y=self.wco_y,
            wco_z=self.wco_z,
            status=self.status,
        )
