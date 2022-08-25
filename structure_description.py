
class EventDetails:
    def __init__(self, LUE_event_id, mass, incoming_u_id, prev_event_id):
        self.LUE_event_id = LUE_event_id
        self.mass = mass
        self.outer_u_ids = []
        self.incoming_u_id = incoming_u_id
        self.prev_event_id = prev_event_id


class StructureDescription:
    def __init__(self):
        self.events_data = {} # event_id: EventDetails
        self.us_data = {}    #  u_id: u
        self.events_order_during_recognition = [] # Порядок обхода событий. Первый в списке распознаем первым.

    def get_event_data(self, event_id):
        event_details = self.events_data[event_id]
        mass = event_details.mass
        prev_event_id=event_details.prev_event_id
        incoming_u = self.us_data[event_details.incoming_u_id]
        return prev_event_id, incoming_u, mass

    def is_first_event(self, event_id):
        return self.events_order_during_recognition[0] == event_id

    def get_event_LUE(self, event_id):
        return self.events_data[event_id].LUE_event_id

    def get_event_LUE_and_mass(self, event_id):
        event_details = self.events_data[event_id]
        return event_details.LUE_event_id, event_details.mass

    def get_incoming_u_id(self,event_id):
        return self.events_data[event_id].incoming_u_id
