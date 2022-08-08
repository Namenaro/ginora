from LUEmemory import *
from common_utils import *
from logger import *

from random import choice, randrange
import matplotlib.pyplot as plt

MAX_RAD = 105

# код постановки единичного эксперимента: ищет ближайшее
# к точке center событие event_id. Возвращает расстояние на до него и данные по нему.
def run_exp(cogmap, center, event_id):
    if event_id not in cogmap.event_ids_set:
        print("no relaxable event in situation...")
        return None, None
    for radius in range(0, MAX_RAD):
        points = get_coords_for_radius(center, radius)
        for point in points:
            if point in cogmap.points_to_events.keys():
                for local_event_id, event_data in cogmap.points_to_events[point].items():
                    if event_data.event_id == event_id:
                        return event_data, radius
    print("no relaxable event in predicted vicinity...")
    return None, None

# для данного события рассматриваются три выборки  - расст. до ближайшего, масса, ошибка
class Samples:
    def __init__(self):
        self.masses =[]
        self.errors = []
        self.relaxation_dists = []

    def add(self, event_data, relaxation_dist):
        if event_data is not None:
            self.relaxation_dists.append(relaxation_dist)
            self.errors.append(event_data.error)
            self.masses.append(event_data.mass_of_seq)
        else:
            self.relaxation_dists.append(-1)


# Собирает и хранит выборки расстояний до ближайшего,
# масс, ошибок для всех событий, упоминаемых в контейнере
class EventStat:
    def __init__(self):
        self.dict_events_samples = {} # {event_id : samples (т.е. объект класса Samples) }

    def fill(self, lue_container, pics, sample_size):
        event_ids = lue_container.get_all_events_ids()
        for event_id in event_ids:
            self.dict_events_samples[event_id]=Samples()

        for i in range(sample_size+1):
            binary_pic = binarise_img(choice(pics))
            cogmap = lue_container.apply_all_to_binary_map(binary_pic, only_save_events2=False)

            x = randrange(0,binary_pic.shape[1] - 1)
            y = randrange(0, binary_pic.shape[0] - 1)
            random_point = Point(x,y)
            for event_id in event_ids:
                event_data, relaxation_dist = run_exp(cogmap, random_point, event_id)
                self.dict_events_samples[event_id].add(event_data, relaxation_dist)

    def draw(self, logger): # отрисовка, чисто для отладки
        for event_id, samples in self.dict_events_samples.items():
            logger.add_text("event_id=" + str(event_id))
            logger.add_text("relaxation_dists=" + str(samples.relaxation_dists))
            fig, ax = plt.subplots()
            num_bins = MAX_RAD + 1
            ax.hist(samples.relaxation_dists,num_bins )
            ax.set_title("relaxation_dists")
            logger.add_fig(fig)

            fig, ax = plt.subplots()
            ax.hist(samples.masses, color='red')
            ax.set_title("masses")
            logger.add_fig(fig)

            logger.add_text("errors=" + str(samples.errors))
            fig, ax = plt.subplots()
            ax.hist(samples.errors, color='green')
            ax.set_title("errors")
            logger.add_fig(fig)


if __name__ == '__main__':
    lue_container = LUEcontainer()
    lue_container.add_rule_1(dx=1, dy=0, max_rad=1)
    lue_container.add_rule_2(dx=0, dy=1, max_rad=10, event1_id=0)
    pics, _, contrast = get_train_test_contrast(class_num=147)

    logger = HtmlLogger("test_events_stat")
    unconditional_stat = EventStat()
    unconditional_stat.fill(lue_container, pics+contrast, sample_size=300)
    unconditional_stat.draw(logger)
    logger.close()







