from common_utils import *

import numpy as np
import matplotlib.pyplot as plt

class EventData:
    def __init__(self, mass_of_seq, event_id):
        self.mass_of_seq = mass_of_seq
        self.event_id = event_id

class Cogmap:
    def __init__(self):
        self.event_ids_set = set()  # типы событий, которые хоть раз регистрировались на этой карте
        self.points_to_events = {}  # {point: {local_event_id: event_data} }
        self.local_id_gen = IdGen()

    def register_event(self, point, event_data):
        self.event_ids_set.add(event_data.event_id)
        if point not in self.points_to_events:
            self.points_to_events[point] = {}
        local_event_id = self.local_id_gen.generate_id()
        self.points_to_events[point][local_event_id] = event_data

    def to_binary_map(self, event_id, map_shape):
        binary_map = np.zeros(map_shape)
        for point, point_events in self.points_to_events.items():
            for local_event_id, event_data in point_events:
                if event_data.event_id == event_id:
                    binary_map[point.y, point.x] = 1
        return binary_map

    def draw(self, back_pic_binary):
        plt.figure()
        cm = plt.get_cmap('seismic')
        plt.imshow(back_pic_binary, cmap=cm, vmin=0, vmax=1)
        list_uniq_event_ids = list(self.event_ids_set)
        cmap = get_cmap(len(list_uniq_event_ids))
        for point, point_events in self.points_to_events.items():
            for local_event_id, event_data in point_events:
                color = cmap(list_uniq_event_ids.index(event_data.event_id))
                marker = '$' + str(event_data.event_id) +'$'
                plt.scatter(point.x, point.y, c=color, marker=marker, alpha=0.4)
        plt.show()


