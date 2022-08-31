from common_utils import get_random_point
from bank_of_physical_samples import MAX_RAD, BankOfPhysicalSamples
from structure_description import *
from structure_exemplar import *
from recognition import *

from random import choice

def unconditional_sample(struct, cogmaps, bank_physical_histograms, sample_size):
    ENERGY_OF_NON_FOUND = -1
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



