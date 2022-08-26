from cogmap import *
from structure_exemplar import *
from ids_generator import StructIdsGenerator
from LUEmemory import *


from copy import deepcopy


class GrowStructure:
    def __init__(self, cogmap):
        self.cogmap = deepcopy(cogmap)
        self.current_exemplar = None
        self.current_structure = None
        self.ids_generator = StructIdsGenerator()

    def get_actual_cogmap(self):
        return self.cogmap

    def get_structure(self):
        return self.current_structure

    def add_first_event(self, cogmap_event_id, incoming_u=None):
        real_coord, event_LUE, mass = self.cogmap.get_event_data(cogmap_event_id)
        #добавляем событие в структуру
        self.current_structure = StructureDescription(self.ids_generator)
        _, event_id = self.current_structure.add_first_event(event_LUE, mass, incoming_u)
        #добавляем событие в экземпляр
        self.current_exemplar = StructureExemplar(self.current_structure)
        self.current_exemplar.set_event_data(event_id, real_coord, mass, incoming_u_error=Point(0,0))
        #удаляем событие из когмап как рассмотренное
        self.cogmap.delete_event(cogmap_event_id)

    def add_next_event(self, cogmap_event_id):
        real_coord, event_LUE, mass = self.cogmap.get_event_data(cogmap_event_id)
        # добавляем событие в структуру, для этого ищем в экземпляре ближайшее событие к данному
        prev_event_id, prev_event_point  = self.current_exemplar.find_event_nearest_to_point(real_coord)
        incoming_u = Point(real_coord.x-prev_event_point.x, real_coord.y-prev_event_point.y)
        incoming_u_id, event_id = self.current_structure.add_next_event(event_LUE, mass, incoming_u, prev_event_id)
        # добавляем событие в экземпляр
        self.current_exemplar.set_event_data(event_id, real_coord, mass, incoming_u_error=Point(0,0))
        # удаляем событие из когмап как рассмотренное
        self.cogmap.delete_event(cogmap_event_id)

if __name__ == '__main__':
    pass