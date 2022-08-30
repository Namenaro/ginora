from cogmap import *
from structure_description import *
from common_utils import Point
from structure_exemplar import *

from copy import deepcopy


def find_exemplar_from_point(cogmap, struct, point):
    new_cogmap = deepcopy(cogmap) # мы будем удалять учтенныe события, а исходную карту повредить нельзя
    exemplar = StructureExemplar(struct)

    for event_id in struct.events_order_during_recognition:
        LUE_id = struct.get_event_LUE(event_id)

        if struct.is_first_event(event_id):
            point_of_prev_event = point
            _,  incoming_u, expected_mass = struct.get_event_data(event_id)
            if incoming_u is None:
                incoming_u = Point(0, 0)
        else:
            prev_event_id, incoming_u, expected_mass = struct.get_event_data(event_id)
            point_of_prev_event = exemplar.get_coord_of_event(prev_event_id)

        predicted_point_of_this_event = Point(point_of_prev_event.x + incoming_u.x, point_of_prev_event.y + incoming_u.y )
        id_in_cogmap, real_coord, real_mass = new_cogmap.find_event_in_cogmap(predicted_point_of_this_event, LUE_id, expected_mass)
        if id_in_cogmap is None:
            return None
        new_cogmap.delete_event(id_in_cogmap)
        incoming_u_error = Point(real_coord.x - predicted_point_of_this_event.x, real_coord.y - predicted_point_of_this_event.y)
        exemplar.set_event_data(event_id, real_coord, real_mass, incoming_u_error)

    return exemplar

if __name__ == '__main__':
    pass

