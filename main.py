from LUEmemory import *
from common_utils import *
from logger import HtmlLogger



if __name__ == '__main__':
    lue_container = LUEcontainer()
    rule1_id = lue_container.add_rule_1(dx=1, dy=0, max_rad=1)
    rule2_id = lue_container.add_rule_2(dx=0, dy=1, max_rad=4, event1_id=0)
    pics, _, _ = get_train_test_contrast(class_num=44)
    cogmaps = []
    i = 0
    for pic in pics:
        binary_map = binarise_img(pic)
        cogmap = lue_container.apply_all_to_binary_map(binary_map)
        print(i)
        i += 1
        cogmaps.append(cogmap)

    logger = HtmlLogger("test")
    for i in range(len(pics)):
        cogmap = cogmaps[i]
        logger.add_fig(cogmap.draw(pics[i]))
    logger.close()
