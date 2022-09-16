from structure_exemplar import *
from structure_description import *
from cogmap import *
from common_utils import Point
from recognition import find_best_exemplar_in_cogmap
from logger import HtmlLogger
from dataset_getter import get_all_for_start
from grow_structure import GrowStructure, create_by_list_of_events
from ids_generator import StructIdsGenerator

from copy import deepcopy
from matplotlib import pyplot as plt


class Merged:
    def __init__(self, exemplar_predictor, exemplar_prediction, bank_of_physical_samples):
        self.predictor_struct = exemplar_predictor.struct_rescription
        self.bank_of_physical_samples = bank_of_physical_samples
        self.merged_struct = deepcopy(exemplar_predictor.struct_rescription)
        merged_exemplar = deepcopy(exemplar_predictor)
        merged_exemplar.struct_rescription = self.merged_struct
        for event_id, coord in exemplar_prediction.events_coords.items():
            closest_event_id_from_predictor, its_point = merged_exemplar.find_event_nearest_to_point(coord)
            incoming_u = Point(coord.x-its_point.x, coord.y-its_point.y)
            mass = exemplar_prediction.get_mass_of_event(event_id)
            event_LUE = exemplar_prediction.get_LUE_of_event(event_id)
            new_incoming_u_id, new_event_id = self.merged_struct.add_next_event(event_LUE, mass, incoming_u, prev_event_id=closest_event_id_from_predictor)
            merged_exemplar.set_event_data(new_event_id, coord, mass, incoming_u_error=Point(0,0))

    def apply(self, cogmap):
        best_exemplar, best_energy = find_best_exemplar_in_cogmap(cogmap, self.merged_struct, self.bank_of_physical_samples)
        return best_exemplar, best_energy

    def show_on_cogmap(self, cogmap, back_pic_binary, ax):
        exemplar, energy = find_best_exemplar_in_cogmap(cogmap, self.merged_struct, self.bank_of_physical_samples)
        ax.title.set_text( "Merged energy: "+ str(energy))
        cm = plt.get_cmap('gray')
        ax.imshow(back_pic_binary, cmap=cm, vmin=0, vmax=1)
        if exemplar is None:
            return
        for event_id, coord in exemplar.events_coords.items():
            marker = '$' + str(event_id) + '$'
            annotation = "(mass=" + str(exemplar.get_mass_of_event(event_id)) + ", LUE=" + str(
                exemplar.get_LUE_of_event(event_id)) + ")"
            color = 'green'
            if event_id in self.predictor_struct.events_order_during_recognition:
                color = 'red'
            ax.scatter(coord.x, coord.y, c=color, marker=marker, alpha=0.8, s=200)
            ax.annotate(annotation, (coord.x, coord.y), color='blue', xytext=(20, 15), textcoords='offset points',
                        ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc=color, alpha=0.6),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.95', color='b'))

            prev_event_id = exemplar.struct_rescription.get_prev_event(event_id)
            if prev_event_id is not None:
                prev_event_coord = exemplar.get_coord_of_event(prev_event_id)
                arrow = mpatches.FancyArrowPatch((prev_event_coord.x, prev_event_coord.y), (coord.x, coord.y),
                                                 mutation_scale=10)
                ax.add_patch(arrow)


    def show_on_cogmaps(self, cogmaps, pics):
        fig, axs = plt.subplots(1, len(pics), figsize=(8*len(pics),8), dpi=60)
        for i in range(len(pics)):
            back_pic_binary = pics[i]
            cogmap = cogmaps[i]
            ax = axs[i]
            self.show_on_cogmap(cogmap, back_pic_binary, ax)
        return fig

    def visualise(self, cogmaps_true, cogmaps_contrast):
        energies_true = []
        for cogmap in cogmaps_true:
            _, energy = self.apply(cogmap)
            energies_true.append(energy)

        energies_contrast = []
        for cogmap in cogmaps_contrast:
            _, energy = self.apply(cogmap)
            energies_contrast.append(energy)
        fig, ax1 = plt.subplots()
        ax1.set_ylabel("Counts")
        ax1.set_xlabel("Energy")

        ax1.hist([energies_true, energies_contrast], color = ['g', 'r'], label=['true class', 'contast'])
        ax1.legend()
        return fig, energies_true, energies_contrast



if __name__ == '__main__':
    ids_gen = StructIdsGenerator()
    class_num = 144
    #logger = HtmlLogger("classifier_test")

    etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps = get_all_for_start(class_num)
    bank_physical_histograms = BankOfPhysicalSamples(contrast_cogmaps + train_cogmaps, cycles=200)

    fig = etalon_cogmap.draw(etalon_pic)
    plt.show()

    predictor_events = [0,5,7]
    prediction_events = [4,3,1]

    exemplar_predictor, _ = create_by_list_of_events(etalon_cogmap, predictor_events, ids_gen)
    exemplar_prediction, _ = create_by_list_of_events(etalon_cogmap, prediction_events, ids_gen)

    merged = Merged(exemplar_predictor, exemplar_prediction, bank_physical_histograms)

    fig = merged.visualise(train_cogmaps, contrast_cogmaps)
    plt.show()
