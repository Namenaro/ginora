class StructIdsGenerator:
    def __init__(self):
        self.i_events = -1
        self.i_us = -1

    def get_id_for_event(self):
        self.i_events += 1
        return self.i_events

    def get_id_for_u(self):
        self.i_us += 1
        return self.i_us