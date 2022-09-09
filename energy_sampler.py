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

from random import choice

np.random.seed(467)
random.seed(47)

def unconditional_sample(struct, cogmaps, bank_physical_histograms, sample_size, ENERGY_OF_NON_FOUND = -1):

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


def conditional_sample(conditional_struct,  cogmaps, bank_physical_histograms, ENERGY_OF_NON_FOUND = -1):
    pass
    #return energy_sample



if __name__ == '__main__':
    class_num = 144


