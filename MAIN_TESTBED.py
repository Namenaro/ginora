from LUEmemory import *
from common_utils import *
from grow_structure import GrowStructure
from bank_of_physical_samples import BankOfPhysicalSamples, MAX_RAD
from recognition import *
from logger import HtmlLogger
from structure_exemplar import *
from energy_sampler import *
from dataset_getter import get_all_for_start

np.random.seed(467)
random.seed(47)

def create_LUE_rules():
    lue_container = LUEcontainer()
    lue_container.add_rule_1(dx=1, dy=0, max_rad=1)  # 0 1 горизонтальная полосочка
    lue_container.add_rule_2(dx=0, dy=1, max_rad=7, event1_id=0)  # 2 3

    lue_container.add_rule_1(dx=0, dy=1, max_rad=1)  # 4 5 вертикальная полосочка
    lue_container.add_rule_2(dx=1, dy=0, max_rad=7, event1_id=4)  # 6 7
    return lue_container

def get_cogmaps_from_rules(lue_container, class_num, contrast_sample_len):
    train_pics, test_pics, contrast_pics = get_train_test_contrast_BIN(class_num, contrast_sample_len)
    cogmaps = []
    for binary_map in train_pics:
        cogmap = lue_container.apply_all_to_binary_map(binary_map, only_save_events2=True)
        cogmaps.append(cogmap)
    etalon_cogmap = cogmaps[0]
    train_cogmaps = cogmaps[1:]
    etalon_pic = train_pics[0]
    train_pics = train_pics[1:]

    contrast_cogmaps = []
    for binary_map in contrast_pics:
        cogmap = lue_container.apply_all_to_binary_map(binary_map, only_save_events2=True)
        contrast_cogmaps.append(cogmap)

    return etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps


def create_exemplar_and_struct_by_events_list(cogmap, events_list):
    struct_creator = GrowStructure(cogmap)
    struct_creator.add_first_event(events_list[0])
    for i in range(1, len(events_list)):
        struct_creator.add_next_event(events_list[i])
    structure = struct_creator.get_structure()
    exemplar = struct_creator.current_exemplar
    return exemplar, structure

def show_LUE_events_stat(LUE_events_list, bank_hists, logger):
    logger.add_text("Каковы вероятности для данного LUE-события 1)массы и 2) нахождения в окрестности радиуса du? ")
    for e_id in LUE_events_list:
        logger.add_text("тип LUE события = " + str(e_id) + ":")
        bank_hists.get_probability_of_mass_of_event(1, 0, e_id)
        bank_hists.get_probability_of_du_of_event(Point(0, 0), e_id)
        logger.add_fig(bank_hists.show_hist_m(e_id))
        logger.add_fig(bank_hists.show_hist_du(e_id))
        logger.add_line_little()

if __name__ == '__main__':
    logger = HtmlLogger("MAIN_TEST")


    # 1. Создание первичных (LUE) правил расстановки событий и разметка ими когнитивных карт:
    lue_rules = create_LUE_rules()
    logger.add_text("LUE-правила связывают пары событий:")
    logger.add_text(lue_rules.print())
    etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps = get_cogmaps_from_rules(lue_rules, class_num=147, contrast_sample_len=20)
    logger.add_text("Эталонная когнитивная карта:")
    logger.add_text(etalon_cogmap.print())
    logger.add_fig(etalon_cogmap.draw(etalon_pic))
    logger.add_line_big()

    # 1.2. Каковы вероятности для данного LUE-события 1)массы и 2) нахождения в окрестности радиуса du?
    LUE_event_ids = [2, 3, 6, 7]
    bank_physical_histograms = BankOfPhysicalSamples(contrast_cogmaps + train_cogmaps, 300)
    show_LUE_events_stat(LUE_event_ids, bank_physical_histograms, logger)
    logger.add_line_big()

    # 2. Хардкодим список событий для предиктора и предсказуемого:
    predictor_events = [3, 2]
    prediction_events = [4,  0, 1]
    logger.add_text(" События предиктора: " + str(predictor_events))
    logger.add_text(" События предсказания: " + str(prediction_events))

    # 3.Создаем стуктуру/экземпляр для предиктора и предсказуемого:
    exemplar_predictor, structure_predictor = create_exemplar_and_struct_by_events_list(etalon_cogmap, predictor_events)
    exemplar_prediction, structure_prediction = create_exemplar_and_struct_by_events_list(etalon_cogmap, prediction_events)
    logger.add_text("Эталонный экземпляр предиктора:")
    logger.add_fig(exemplar_predictor.show(etalon_pic))
    logger.add_text("Эталонный экземпляр предсказания:")
    logger.add_fig(exemplar_prediction.show(etalon_pic))

    # 4. Максимальная энергия того и того:
    IDEAL_ENERGY_PREDICTOR = exemplar_predictor.get_exemplar_energy(bank_physical_histograms)
    logger.add_text("Энергия идеального экземпляра предиктора = " + str(IDEAL_ENERGY_PREDICTOR))
    IDEAL_ENERGY_PREDICTION = exemplar_prediction.get_exemplar_energy(bank_physical_histograms)
    logger.add_text("Энергия идеального экземпляра предискауемого = " + str(IDEAL_ENERGY_PREDICTION))
    logger.add_line_big()



    logger.close()


