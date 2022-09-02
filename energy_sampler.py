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

def visualise_energy_unconditional(struct_size, class_num=147):
    # визуально отвечаем на вопрос, правда ли, что чем сложнее структура, тем реже низкие значения ее энергий в безусловной выбоорке?
    logger = HtmlLogger("energy_"+str(struct_size))
    num_of_test_structs = 5
    size_of_sample = 300
    etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps = get_all_for_start(class_num)

    for j in range(num_of_test_structs):

        #выбираем на когмапе наугад struct_size штук событий
        # создаем на их основе структуру
        struct_creator = GrowStructure(etalon_cogmap)
        cogmap_fisrt_event_id = struct_creator.get_actual_cogmap().get_random_event()
        struct_creator.add_first_event(cogmap_fisrt_event_id)
        for i in range(1, struct_size):
            cogmap_event_id = struct_creator.get_actual_cogmap().get_random_event()
            struct_creator.add_next_event(cogmap_event_id)
            if cogmap_event_id is None:
                print ("TOO LARGE STRUCT for this etalon cogmap")
                return
        structure = struct_creator.get_structure()


        # добавляем в лог ее идеальный экземпляр картинкой
        point, _, _ = etalon_cogmap.get_event_data(cogmap_fisrt_event_id)
        exemplar = find_exemplar_from_point(etalon_cogmap, structure, point)
        fig = exemplar.show(etalon_pic)
        logger.add_fig(fig)

        # собираем по ней безусловную выборку и ее гисту в лог
        bank_physical_histograms = BankOfPhysicalSamples(contrast_cogmaps + train_cogmaps, cycles=200)
        energy_sample = unconditional_sample(structure, contrast_cogmaps + train_cogmaps, bank_physical_histograms,
                                             sample_size=size_of_sample)
        fig = visualise_sample(energy_sample, n_bins=11)
        logger.add_fig(fig)
        logger.add_text("---------------------------Next structure:----------------------------")
    logger.close()

if __name__ == '__main__':
    class_num = 144
    visualise_energy_unconditional(1, class_num)
    visualise_energy_unconditional(2, class_num)
    visualise_energy_unconditional(3, class_num)
    visualise_energy_unconditional(4, class_num)
    visualise_energy_unconditional(5, class_num)

