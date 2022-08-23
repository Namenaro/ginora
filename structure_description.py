
class EventDetails:
    def __init__(self, LUE_event_id, mass, mass_id, u_id=None):
        self.LUE_event_id = LUE_event_id
        self.mass = mass
        self.mass_id = mass_id
        self.u_id = u_id # исходящее u или None

class UDetails:
    def __init__(self, u, start_event_id, end_event_id):
        self.u = u
        self.start_event_id= start_event_id
        self.end_event_id = end_event_id

class StructureDescription:
    def __init__(self):
        self.events_data = {} # event_id: event_details
        self.us_data = {}    #  u_id: u_details
        self.events_order_during_recognition = [] # упорядоченные event_ids. Первый в списке распознаем первым.

    def add_entry(self,  u, start_event_id, end_event_id, LUE_event_id, mass, mass_id, event_id, u_id):
        self.events_order_during_recognition.append(event_id)
        self.events_data[event_id]=EventDetails(LUE_event_id, mass, mass_id)
        self.us_data[u_id]=UDetails(u, start_event_id, end_event_id)
        self.events_data[start_event_id].u_id = u_id

