from ids_generator import StructIdsGenerator


class EventDetails:
    def __init__(self, LUE_event_id, mass, incoming_u_id, prev_event_id):
        self.LUE_event_id = LUE_event_id
        self.mass = mass
        self.outer_u_ids = []
        self.incoming_u_id = incoming_u_id
        self.prev_event_id = prev_event_id


class StructureDescription:
    def __init__(self, ids_gen):
        self.ids_gen = ids_gen
        self.events_data = {}  # event_id: EventDetails
        self.us_data = {}    #  u_id: u
        self.events_order_during_recognition = [] # Порядок обхода событий. Первый в списке распознаем первым.

    def get_event_data(self, event_id):
        event_details = self.events_data[event_id]
        mass = event_details.mass
        prev_event_id=event_details.prev_event_id
        if event_details.incoming_u_id is not None:
            incoming_u = self.us_data[event_details.incoming_u_id]
        else:
            incoming_u = None
        return prev_event_id, incoming_u, mass

    def is_first_event(self, event_id):
        return self.events_order_during_recognition[0] == event_id

    def get_first_event_LUE(self):
        first_event_id = self.events_order_during_recognition[0]
        LUE_id = self.events_data[first_event_id].LUE_event_id
        return LUE_id

    def get_event_LUE(self, event_id):
        return self.events_data[event_id].LUE_event_id

    def get_event_LUE_and_mass(self, event_id):
        event_details = self.events_data[event_id]
        return event_details.LUE_event_id, event_details.mass

    def get_incoming_u_id(self,event_id):
        return self.events_data[event_id].incoming_u_id

    def add_first_event(self, event_LUE, mass, incoming_u):
        if incoming_u is None:
            incoming_u_id = None
        else:
            incoming_u_id = self.ids_gen.get_id_for_u()
        event_id = self.ids_gen.get_id_for_event()
        prev_event_id = None
        self._add_event(event_id, event_LUE, mass, incoming_u, incoming_u_id, prev_event_id)
        return incoming_u_id, event_id

    def add_next_event(self, event_LUE, mass, incoming_u, prev_event_id):
        incoming_u_id = self.ids_gen.get_id_for_u()
        event_id = self.ids_gen.get_id_for_event()
        self._add_event(event_id, event_LUE, mass, incoming_u, incoming_u_id, prev_event_id)
        return incoming_u_id, event_id

    def _add_event(self, event_id, event_LUE, mass, incoming_u, incoming_u_id, prev_event_id):
        self.events_order_during_recognition.append(event_id)
        self.events_data[event_id]=EventDetails(event_LUE, mass, incoming_u_id, prev_event_id)
        if incoming_u_id is not None:
            self.us_data[incoming_u_id]=incoming_u
        if prev_event_id is not None:
            self.events_data[prev_event_id].outer_u_ids.append(incoming_u_id)

    def get_LUE_id_of_end_of_u(self, u_id):
        for event_id, event_details in self.events_data.items():
            if event_details.incoming_u_id == u_id:
                return event_details.LUE_event_id



