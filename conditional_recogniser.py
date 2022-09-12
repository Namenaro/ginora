from structure_exemplar import *
from structure_description import *
from common_utils import *


from copy import deepcopy


class ConditionalRecogniser:
    def __init__(self, exemplar_predictor, exemplar_prediction):
        self.unconditional_struct_of_prediction = exemplar_prediction.struct_rescription
        # сначала заполним смерженную структуру
        merged_struct = deepcopy(exemplar_predictor.struct_rescription)
        merged_exemplar = deepcopy(exemplar_predictor)
        merged_exemplar.struct_rescription = merged_struct

        for event_id, coord in exemplar_prediction.events_coords.items():
            closest_event, its_point = merged_exemplar.find_event_nearest_to_point(coord)
            incoming_u = Point(coord.x - its_point.x, coord.y - its_point.y)
            mass = exemplar_prediction.get_mass_of_event(event_id)
            event_LUE = exemplar_prediction.get_LUE_of_event(event_id)
            new_incoming_u_id, new_event_id = merged_struct.add_next_event(event_LUE, mass, incoming_u,
                                                                                prev_event_id=closest_event, event_id=event_id)
            merged_exemplar.set_event_data(new_event_id, coord, mass, incoming_u_error=Point(0, 0))

        # теперь обходим все события предсказания и смотрим, у кого из них
            # поменялось предшествующее событие
        self.conditional_prediction_struct = deepcopy(exemplar_prediction.struct_rescription)
        for event_id, coord in exemplar_prediction.events_coords.items():
            prev_event_old = self.unconditional_struct_of_prediction.get_prev_event(event_id)
            prev_event_new = merged_struct.get_prev_event(event_id)
            if prev_event_new != prev_event_old:
                prev_event_coord = merged_exemplar.get_coord_of_event(prev_event_new)
                new_u = Point(coord.x -prev_event_coord.x, coord.y -prev_event_coord.y)
                self.conditional_prediction_struct.reset_input_to_event(event_id=event_id,
                                                                        new_input_u=new_u,
                                                       new_prev_event=prev_event_new)


    def apply(self, exemplar_predictor, cogmap):
        exemplar = StructureExemplar(self.conditional_prediction_struct)

        undone_events = deepcopy(self.conditional_prediction_struct.events_order_during_recognition)
        while True:
            if len(undone_events) == 0:
                break
            for event_id in undone_events:
                prev_event_id = self.conditional_prediction_struct.get_prev_event(event_id)
                if prev_event_id in undone_events:
                    continue
                undone_events.remove(event_id)

                LUE_id = self.conditional_prediction_struct.get_event_LUE(event_id)
                _, incoming_u, expected_mass = self.conditional_prediction_struct.get_event_data(event_id)

                # ищем  point_of_prev_event: либо в экземпляре предиктора, либо v уже заполненной части экземпляра предсказания
                if prev_event_id in self.conditional_prediction_struct.events_order_during_recognition:
                    point_of_prev_event = exemplar.get_coord_of_event(prev_event_id)
                else:
                    point_of_prev_event = exemplar_predictor.get_coord_of_event(prev_event_id)

                # ищем нужное событие на когмап и заполняем экземпляр
                predicted_point_of_this_event = Point(point_of_prev_event.x + incoming_u.x,
                                                      point_of_prev_event.y + incoming_u.y)
                id_in_cogmap, real_coord, real_mass = cogmap.find_event_in_cogmap(predicted_point_of_this_event, LUE_id,
                                                                                      expected_mass)
                if id_in_cogmap is None:
                    return None

                incoming_u_error = Point(real_coord.x - predicted_point_of_this_event.x,
                                         real_coord.y - predicted_point_of_this_event.y)
                exemplar.set_event_data(event_id, real_coord, real_mass, incoming_u_error)

        return exemplar


if __name__ == '__main__':
    pass