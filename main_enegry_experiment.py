

from LUEmemory import *
from common_utils import *
from grow_structure import GrowStructure
from bank_of_physical_samples import BankOfPhysicalSamples, MAX_RAD
from recognition import *
from logger import HtmlLogger
from energy_sampler import *
from dataset_getter import get_all_for_start

np.random.seed(467)
random.seed(47)


if __name__ == '__main__':

    etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps = get_all_for_start(class_num=147)
    fig = etalon_cogmap.draw(etalon_pic)
    plt.show()

    #создаем структуру:
    cogmap_events_selected =[2,4]
    struct_creator = GrowStructure(etalon_cogmap)
    struct_creator.add_first_event(cogmap_events_selected[0])
    for i in range(1, len(cogmap_events_selected)):
        struct_creator.add_next_event(cogmap_events_selected[i])
    structure = struct_creator.get_structure()

    #простестируем, что она распознавается, если знать почти верную точку:
    point , _, _ = etalon_cogmap.get_event_data(cogmap_events_selected[0])
    point.x+=2
    point.y+=1
    exemplar = find_exemplar_from_point(etalon_cogmap, structure, point)
    exemplar.show(etalon_pic)
    plt.show()

    bank_physical_histograms = BankOfPhysicalSamples(contrast_cogmaps+train_cogmaps)
    energy = exemplar.get_exemplar_energy(bank_physical_histograms)
    print ("exemplar energy (max for this struct) = " + str(energy))

    # протестируем, сбор выборки бузусловной
    energy_sample = unconditional_sample(structure, contrast_cogmaps+train_cogmaps, bank_physical_histograms, sample_size=770)
    visualise_sample(energy_sample, n_bins=7)
    plt.show()
