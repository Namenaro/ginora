import copy

from common_utils import get_random_point
from bank_of_physical_samples import MAX_RAD, BankOfPhysicalSamples
from structure_description import *
from structure_exemplar import *
from recognition import *
from logger import HtmlLogger
from dataset_getter import get_all_for_start
from cogmap import *
from grow_structure import *
from main_constants import *


from conditional_recogniser import ConditionalRecogniser

from random import choice

np.random.seed(467)
random.seed(47)

def unconditional_sample(struct, cogmaps, bank_physical_histograms, sample_size):

    energy_sample = []

    for i in range(sample_size):
        random_cogmap = choice(cogmaps)
        random_point = get_random_point()


        exemplar = find_exemplar_from_point(random_cogmap, struct, random_point)
        if exemplar is None:
            energy_sample.append(ENERGY_OF_NON_FOUND)
        else:
            energy = exemplar.get_exemplar_energy(bank_physical_histograms)
            energy_sample.append(energy)
    return energy_sample


def conditional_sample(conditional_struct, predictor_struct,  cogmaps, bank_physical_histograms):
    energy_sample_predictor = []
    energy_sample_prediction = []
    for cogmap in cogmaps:
        exemplar_predictor, predictor_energy = find_best_exemplar_in_cogmap(cogmap, predictor_struct, bank_physical_histograms)
        if exemplar_predictor is None:
            energy_sample_predictor.append(ENERGY_OF_NON_FOUND)
            conditional_exemplar_prediction, prediction_energy = find_best_exemplar_in_cogmap(cogmap, conditional_struct.unconditional_struct_of_prediction, bank_physical_histograms)
        else:
            energy_sample_predictor.append(predictor_energy)
            conditional_exemplar_prediction = conditional_struct.apply(exemplar_predictor, cogmap)
            prediction_energy = conditional_exemplar_prediction.get_exemplar_energy(bank_physical_histograms)

        energy_sample_prediction.append(prediction_energy)

    return energy_sample_predictor, energy_sample_prediction



if __name__ == '__main__':
    ids_gen = StructIdsGenerator()
    class_num = 144

    etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps = get_all_for_start(class_num)
    bank_physical_histograms = BankOfPhysicalSamples(contrast_cogmaps + train_cogmaps, cycles=200)

    fig = etalon_cogmap.draw(etalon_pic)
    plt.show()

    predictor_events = [0, 2]
    prediction_events = [4, 3, 1]

    exemplar_predictor, predictor_struct = create_by_list_of_events(etalon_cogmap, predictor_events, ids_gen)
    exemplar_prediction, _ = create_by_list_of_events(etalon_cogmap, prediction_events, ids_gen)

    cond_rec = ConditionalRecogniser(exemplar_predictor, exemplar_prediction)

    energy_sample_predictor, energy_sample_prediction = conditional_sample(cond_rec, predictor_struct, train_cogmaps+contrast_cogmaps, bank_physical_histograms)

    fig, ax1 = plt.subplots()
    ax1.set_ylabel("Counts")
    ax1.set_xlabel("Energy")

    ax1.hist(energy_sample_prediction)
    plt.show()

    fig, ax1 = plt.subplots()
    ax1.plot(energy_sample_prediction, 'g')
    ax1.plot(energy_sample_predictor, 'r')
    plt.show()


