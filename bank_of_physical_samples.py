

from events_stat import *
from tqdm import tqdm

MAX_RAD = 105


class BankOfPhysicalSamples:
    def __init__(self, cogmaps):
        self.cogmaps = cogmaps
        self.dict_events_to_dus = {}
        self.dict_event_to_masses = {}

        self.num_bins = None

    @staticmethod
    def rand_point():
        X = random.randint(0, MAX_RAD)
        Y = random.randint(0, MAX_RAD)
        point = Point(X, Y)
        return point

    @staticmethod
    def get_counts(N, rads):
        MAX = np.max(rads)
        counter = {}
        for i in range(0, MAX):
            counter[i] = 0

        for i in range(0, N):
            cur_rad = rads[i]
            for j in range(cur_rad, MAX):
                counter[j] += 1

        return counter

    @staticmethod
    def get_probs(N, counter):

        keys = []
        probs = []

        for key, val in counter.items():
            keys.append(key)
            probs.append(val / N)

        return keys, probs

    def get_probability_of_mass_of_event(self, etalon_m, dm, event_id):
        all_masses = []

        if event_id not in self.dict_event_to_masses.keys():

            for cogmap in self.cogmaps:
                for point, point_events in cogmap.points_to_events.items():
                    for local_event_id, event_data in point_events.items():
                        if event_data.event_id == event_id:
                            all_masses.append(event_data.mass_of_seq)

            unique_masses = list(set(all_masses))
            self.num_bins = len(unique_masses)

            indexes = []
            for i in range(len(unique_masses)):
                if etalon_m - dm <= unique_masses[i] <= etalon_m + dm:
                    indexes.append(i)

            hist_result = np.histogram(all_masses, bins=self.num_bins,
                                       weights=np.ones_like(all_masses) / len(all_masses))
            dict_value = (hist_result[0], hist_result[1], all_masses)

            self.dict_event_to_masses[event_id] = dict_value
            all_probs = hist_result[0]

            prob = 0
            for i in range(indexes[0], indexes[-1] + 1):
                prob += all_probs[i]

        else:
            hist_result = self.dict_event_to_masses[event_id]
            all_masses = hist_result[2]
            unique_masses = list(set(all_masses))

            indexes = []
            for i in range(len(unique_masses)):
                if etalon_m - dm <= unique_masses[i] <= etalon_m + dm:
                    indexes.append(i)

            all_probs = hist_result[0]
            prob = 0
            for i in range(indexes[0], indexes[-1] + 1):
                prob += all_probs[i]

        return prob

    def get_probability_of_du_of_event(self, du, event_id):
        all_rads = []
        my_rad = du.x + du.y
        rand_point = self.rand_point()
        if event_id not in self.dict_events_to_dus.keys():

            for cogmap in self.cogmaps:
                for point, point_events in cogmap.points_to_events.items():
                    for local_event_id, event_data in point_events.items():
                        if event_data.event_id == event_id:
                            coords = Point(rand_point.x + du.x, rand_point.y + du.y)
                            _, radius = run_exp(cogmap, coords, event_id)
                            if radius is not None:
                                all_rads.append(radius)
            N = len(all_rads)
            counter = self.get_counts(N, all_rads)
            rads, probs = self.get_probs(N, counter)
            dict_value = (rads, probs)
            self.dict_events_to_dus[event_id] = dict_value

            for i in range(len(rads)):
                if rads[i] == my_rad:
                    prob = probs[i]
        else:
            rads, probs = self.dict_events_to_dus[event_id]
            for i in range(len(rads)):
                if rads[i] == my_rad:
                    prob = probs[i]
        return prob

    def show_hist_m(self, event_id):
        fig, ax = plt.subplots()
        all_masses = self.dict_event_to_masses[event_id][2]

        ax.hist(all_masses, edgecolor="black", bins=self.num_bins,
                weights=np.ones_like(all_masses) / len(all_masses))
        plt.show()

    def show_hist_du(self, event_id):

        keys, probs = self.dict_events_to_dus[event_id]
        pos = np.arange(len(keys))
        width = 1.0  # gives histogram aspect to the bar diagram

        ax = plt.axes()
        ax.set_xticks(pos + (width / 2))
        ax.set_xticklabels(keys)

        plt.bar(pos, probs, width, edgecolor="black")
        plt.show()


def create_LUE_container():
    lue_container = LUEcontainer()
    lue_container.add_rule_1(dx=1, dy=0, max_rad=1)  # 0 1 горизонтальная полосочка
    lue_container.add_rule_2(dx=0, dy=1, max_rad=7, event1_id=0)  # 2 3
    lue_container.add_rule_2(dx=1, dy=1, max_rad=3, event1_id=0)  # 4 5

    lue_container.add_rule_1(dx=0, dy=1, max_rad=1)  # 6 7 вертикальная полосочка
    lue_container.add_rule_2(dx=1, dy=0, max_rad=7, event1_id=7)  # 8 9
    return lue_container


def create_cogmaps(lue_container, pics):
    cogmaps = []
    for pic in tqdm(pics):
        binary_map = binarise_img(pic)
        cogmap = lue_container.apply_all_to_binary_map(binary_map, only_save_events2=True)
        cogmaps.append(cogmap)
    return cogmaps


def main():
    lue_container_2 = create_LUE_container()

    # получение картинок данного типа + контрастных (т.е. других типов вперемешку)
    _, _, contrast_pics = get_train_test_contrast(class_num=8)

    # для каждой трейновой картинки создаем когнитивную
    # карту и заполняем ее точками согласно праввилам из lue_container:
    contrast_cogmaps = create_cogmaps(lue_container_2, contrast_pics)

    bank =BankOfPhysicalSamples(contrast_cogmaps)
    event_id = 2

    print(bank.get_probability_of_mass_of_event(5, 2, event_id))
    print(bank.get_probability_of_du_of_event(Point(11, 4), event_id))

    bank.show_hist_m(event_id)
    bank.show_hist_du(event_id)


if __name__ == '__main__':
    main()

# fig, (ax1, ax2) = plt.subplots(1, 2)
