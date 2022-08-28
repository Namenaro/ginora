from LUEmemory import *
from common_utils import *
from logger import HtmlLogger
from events_stat import *

def create_LUE_container():
    lue_container = LUEcontainer()
    lue_container.add_rule_1(dx=1, dy=0, max_rad=1)  #0 1 горизонтальная полосочка
    lue_container.add_rule_2(dx=0, dy=1, max_rad=7, event1_id=0) #2 3
    lue_container.add_rule_2(dx=1, dy=1, max_rad=3, event1_id=0) #4 5

    lue_container.add_rule_1(dx=0, dy=1, max_rad=1) #6 7 вертикальная полосочка
    lue_container.add_rule_2(dx=1, dy=0, max_rad=7, event1_id=7)  # 8 9

    return lue_container

def create_cogmaps(lue_container, pics):
    cogmaps = []
    i = 0
    for pic in pics:
        binary_map = binarise_img(pic)
        cogmap = lue_container.apply_all_to_binary_map(binary_map, only_save_events2=True)
        print(i)
        i += 1
        cogmaps.append(cogmap)
    return cogmaps

if __name__ == '__main__':
    # добавление вручную правил детекции нечетких последовательностей
    lue_container =create_LUE_container()

    # получение картинок данного типа + контрастных (т.е. других типов вперемешку)
    train_pics, test_pics, contrast_pics = get_train_test_contrast(class_num=147)

    # для каждой трейновой картинки создаем когнитивную
    # карту и заполняем ее точками согласно праввилам из lue_container:
    cogmaps = create_cogmaps(lue_container, train_pics)

    # отрисовка когнитивных карт в хтмл-ку (чисто для отладки)
    logger = HtmlLogger("test")
    for i in range(len(pics)):
        cogmap = cogmaps[i]
        logger.add_fig(cogmap.draw(pics[i]))
    logger.close()

    # сбор статистических данных обо всех типих точек до обучения
    unconditional_stat = EventStat()
    unconditional_stat.fill(lue_container, train_pics + contrast_pics, sample_size=200)

    # отрисовка этих стат.данных в хтмл-ку ввиде гистограмм (чисто для отладки)
    logger = HtmlLogger("test_events_stat")
    unconditional_stat.draw(logger)
    logger.close()
