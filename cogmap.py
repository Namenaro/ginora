from common_utils import *

import numpy as np
import matplotlib.pyplot as plt

class EventData:
    def __init__(self, mass_of_seq, event_id, error):
        self.mass_of_seq = mass_of_seq
        self.event_id = event_id #LUE
        self.error = error

class Cogmap:
    def __init__(self):
        self.event_ids_set = set()  # типы LUE-событий, которые хоть раз регистрировались на этой карте
        self.points_to_events = {}  # {point: {local_event_id: event_data} }
        self.local_id_gen = IdGen()
        self.num_events_in_cogmap =0

    def register_event(self, point, event_data):
        self.event_ids_set.add(event_data.event_id)
        if point not in self.points_to_events:
            self.points_to_events[point] = {}
        local_event_id = self.local_id_gen.generate_id()
        self.points_to_events[point][local_event_id] = event_data
        self.num_events_in_cogmap+=1

    def to_binary_map(self, event_id, map_shape):
        binary_map = np.zeros(map_shape)
        for point, point_events in self.points_to_events.items():
            for local_event_id, event_data in point_events.items():
                if event_data.event_id == event_id:
                    binary_map[point.y, point.x] = 1
        return binary_map

    def draw(self, back_pic_binary):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        cm = plt.get_cmap('gray')
        ax1.imshow(back_pic_binary, cmap=cm, vmin=0, vmax=1)
        ax1.set_title("LUE ids")
        ax2.imshow(back_pic_binary, cmap=cm, vmin=0, vmax=1)
        ax2.set_title("ids in THIS cogmap")
        list_uniq_event_ids = list(self.event_ids_set)
        cmap = get_cmap(len(list_uniq_event_ids)+1)
        for point, point_events in self.points_to_events.items():
            for local_event_id, event_data in point_events.items():
                color_num = list_uniq_event_ids.index(event_data.event_id)
                print(color_num)
                color = cmap(color_num)
                marker = '$' + str(event_data.event_id) +'$'
                ax1.scatter(point.x, point.y, c=[color], marker=marker, alpha=0.5, s=100)
                marker = '$' + str(local_event_id) +'$'
                ax2.scatter(point.x, point.y, c='green', marker=marker, alpha=0.5, s=100)
        return fig

    def find_event_in_cogmap(self, predicted_point_of_this_event, LUE_id, expected_mass, max_rad=105):
        # return id_in_cogmap, real_coord, real_mass  или None, None, None
        # TODO: пока не используется expected_mass
        if LUE_id not in self.event_ids_set:
            return None, None, None

        for radius in range(0, max_rad):
            points = get_coords_for_radius(predicted_point_of_this_event, radius)

            for point in points:
                if point in self.points_to_events.keys():
                    for local_event_id, event_data in self.points_to_events[point].items():
                        if event_data.event_id == LUE_id:
                            return local_event_id, point, event_data.mass_of_seq
        return None, None, None


    def delete_event(self, id_in_cogmap):
        for point, events_in_point in self.points_to_events.items():
            if id_in_cogmap in events_in_point:
                del events_in_point[id_in_cogmap]
                break
        if not events_in_point:
            del self.points_to_events[point]
        self.num_events_in_cogmap-= 1

    def get_event_data(self, event_id_in_cogmap):
        for point, point_events in self.points_to_events.items():
            for local_event_id, event_data in point_events.items():
                if event_id_in_cogmap == local_event_id:
                    return point, event_data.event_id, event_data.mass_of_seq
        return None,None,None

    def get_random_event(self):
        if self.num_events_in_cogmap==0:
            return None

        point = random.choice(list(self.points_to_events.keys()))
        event_local_id = random.choice(list(self.points_to_events[point]))
        return event_local_id

    def get_all_points_for_LUE(self, LUE_id):
        points = []
        if LUE_id not in self.event_ids_set:
            return []
        for point, point_events in self.points_to_events.items():
            for local_event_id, event_data in point_events.items():
                if event_data.event_id == LUE_id:
                    points.append(point)
        return points

    def print(self):
        description = ""
        for point, point_events in self.points_to_events.items():
            for local_event_id, event_data in point_events.items():
                event_descript = "id в ког.мапе: "+ str(local_event_id) +" [LUE_id="+ str(event_data.event_id) +" , mass=" + str(event_data.mass_of_seq)  +"] "+str(point)+ "<br>"
                description +=event_descript
        return description


