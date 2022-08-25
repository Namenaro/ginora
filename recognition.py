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
                incoming_u = Point(0,0)
        else:
            prev_event_id, incoming_u, expected_mass = struct.get_event_data(event_id)
            point_of_prev_event = exemplar.get_coord_of_event(prev_event_id)

        predicted_point_of_this_event = point_of_prev_event + incoming_u
        id_in_cogmap, real_coord, real_mass = new_cogmap.find_event_in_cogmap(predicted_point_of_this_event, LUE_id, expected_mass)
        if id_in_cogmap is None:
            return None
        new_cogmap.delete_event(id_in_cogmap)
        incoming_u_error = real_coord - predicted_point_of_this_event
        exemplar.set_event_data(event_id, real_coord, real_mass, incoming_u_error)

    return exemplar

if __name__ == '__main__':
    # ШАГ_1
    # дописать 2 метода в когмап (где ТУДУ)
    # создать вручную описание структуры (вызовы функций exemplar.add_event_from_cogmap (cogmap, event_id_in_cogmap, ids_generator)
    # визуализировать ее экземпляр на эталонной картинке и на других (exemplar.show(back_pick,cogmap,exemplar)
    # взять код Ильи
    # собрать безусловную выюорку и показать ее гистограмму (для структур разной сложности)

    #------------------------------------------
    # ШАГ_2
    # создать вручную структуру-предиктор и собрать условную выборку
    # посмотреть п-значения

    #-------------------------------------
    # ШАГ_3
    # организовать рост с замером п-значений
    # энергия релаксации совместной структуры
