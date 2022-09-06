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
from energy_sampler import unconditional_sample

from random import choice

np.random.seed(467)
random.seed(47)

def visualise_formula(struct_size=3, class_num=147, energy_range=[-1,10], n_bins=11, ENERGY_OF_NON_FOUND=-1):
    logger = HtmlLogger("formula_energy_"+str(struct_size))
    num_of_test_structs = 1
    n_cogmaps = 5

    etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps = get_all_for_start(class_num)
    bank_physical_histograms = BankOfPhysicalSamples(contrast_cogmaps + train_cogmaps, cycles=200)
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
        logger.add_text("ideal exemplar of this structure:")
        point, _, _ = etalon_cogmap.get_event_data(cogmap_fisrt_event_id)
        exemplar = find_exemplar_from_point(etalon_cogmap, structure, point)
        fig = exemplar.show(etalon_pic)
        logger.add_fig(fig)
        ideal_energy = exemplar.get_exemplar_energy(bank_physical_histograms)
        logger.add_text("ideal energy= " + str(ideal_energy))


        # собираем по ней безусловную выборку и ее гисту в лог
        logger.add_text("unconditional sample (histogram) of this structure:")
        energy_sample = unconditional_sample(structure, contrast_cogmaps + train_cogmaps, bank_physical_histograms,
                                             sample_size=200, ENERGY_OF_NON_FOUND=ENERGY_OF_NON_FOUND)
        fig = visualise_sample(energy_sample, energy_range, n_bins)
        logger.add_fig(fig)
        logger.add_text("struct finding on conctere cogmaps:")
        visualise_struct_recogmition_on_several_cogmaps(structure, train_cogmaps[:n_cogmaps], train_pics[:n_cogmaps],
                                                        bank_physical_histograms, logger, energy_range)


        logger.add_text("---------------------------Next structure:----------------------------")
    logger.close()

if __name__ == '__main__':
    class_num = 147
    energy_range = [-1, 10]
    n_bins = 11
    ENERGY_OF_NON_FOUND = -1
    visualise_formula(1, class_num, energy_range, n_bins, ENERGY_OF_NON_FOUND)
    visualise_formula(2, class_num, energy_range, n_bins, ENERGY_OF_NON_FOUND)
    visualise_formula(3, class_num, energy_range, n_bins, ENERGY_OF_NON_FOUND)
