from LUEmemory import *
from common_utils import *
from grow_structure import GrowStructure
from bank_of_physical_samples import BankOfPhysicalSamples, MAX_RAD
from recognition import *
from logger import HtmlLogger
from energy_sampler import *


def get_all_for_start(class_num=147):
    lue_container = LUEcontainer()
    lue_container.add_rule_1(dx=1, dy=0, max_rad=1)  # 0 1 горизонтальная полосочка
    lue_container.add_rule_2(dx=0, dy=1, max_rad=7, event1_id=0)  # 2 3

    lue_container.add_rule_1(dx=0, dy=1, max_rad=1)  # 4 5 вертикальная полосочка
    lue_container.add_rule_2(dx=1, dy=0, max_rad=7, event1_id=7)  # 6 7

    train_pics, test_pics, contrast_pics = get_train_test_contrast_BIN(class_num)
    cogmaps = []
    for binary_map in train_pics:
        cogmap = lue_container.apply_all_to_binary_map(binary_map, only_save_events2=True)
        cogmaps.append(cogmap)
    etalon_cogmap = cogmaps[0]
    train_cogmaps = cogmaps[1:]
    etalon_pic = train_pics[0]
    train_pics = train_pics[1:]

    contrast_cogmaps =[]
    for binary_map in contrast_cogmaps:
        cogmap = lue_container.apply_all_to_binary_map(binary_map, only_save_events2=True)
        contrast_cogmaps.append(cogmap)

    return etalon_cogmap,etalon_pic, train_cogmaps, train_pics, contrast_cogmaps


if __name__ == '__main__':
    etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps = get_all_for_start(class_num=147)
    fig = etalon_cogmap.draw(etalon_pic)
    plt.show()

    #создаем структуру:
    cogmap_events_selected =[2,3]
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
    energy_sample = unconditional_sample(structure, contrast_cogmaps+train_cogmaps, bank_physical_histograms, sample_size=10)
    visualise_sample(energy_sample, n_bins=5)
    plt.show()
