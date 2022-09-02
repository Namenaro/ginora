from LUEmemory import *
from common_utils import get_train_test_contrast_BIN

np.random.seed(467)
random.seed(47)

def get_all_for_start(class_num=147, contrast_sample_len=40):
    lue_container = LUEcontainer()
    lue_container.add_rule_1(dx=1, dy=0, max_rad=1)  # 0 1 горизонтальная полосочка
    lue_container.add_rule_2(dx=0, dy=1, max_rad=7, event1_id=0)  # 2 3

    lue_container.add_rule_1(dx=0, dy=1, max_rad=1)  # 4 5 вертикальная полосочка
    lue_container.add_rule_2(dx=1, dy=0, max_rad=7, event1_id=4)  # 6 7

    train_pics, test_pics, contrast_pics = get_train_test_contrast_BIN(class_num, contrast_sample_len)
    cogmaps = []
    for binary_map in train_pics:
        cogmap = lue_container.apply_all_to_binary_map(binary_map, only_save_events2=True)
        cogmaps.append(cogmap)
    etalon_cogmap = cogmaps[0]
    train_cogmaps = cogmaps[1:]
    etalon_pic = train_pics[0]
    train_pics = train_pics[1:]

    contrast_cogmaps =[]
    for binary_map in contrast_pics:
        cogmap = lue_container.apply_all_to_binary_map(binary_map, only_save_events2=True)
        contrast_cogmaps.append(cogmap)

    return etalon_cogmap,etalon_pic, train_cogmaps, train_pics, contrast_cogmaps
