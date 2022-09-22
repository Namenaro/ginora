from LUEmemory import *
from common_utils import *
from grow_structure import GrowStructure
from bank_of_physical_samples import BankOfPhysicalSamples, MAX_RAD
from recognition import *
from logger import HtmlLogger
from structure_exemplar import *
from energy_sampler import *
from dataset_getter import get_all_for_start
from stata import get_p_value_for_two_samples
from classifier import Merged
from main_constants import *

np.random.seed(467)
random.seed(47)

def create_LUE_rules():
    lue_container = LUEcontainer()
    lue_container.add_rule_1(dx=1, dy=0, max_rad=1)  # 0 1 горизонтальная полосочка
    lue_container.add_rule_1(dx=0, dy=1, max_rad=1)  # 2 3 вертикальная полосочка

    lue_container.add_rule_2(dx=0, dy=1, max_rad=7, event1_id=0)  # 4 5
    lue_container.add_rule_2(dx=1, dy=0, max_rad=7, event1_id=4)  # 6 7
    lue_container.add_rule_2(dx=1, dy=0, max_rad=3, event1_id=6)  # 8 9
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


def create_exemplar_and_struct_by_events_list(cogmap, events_list, ids_gen):
    struct_creator = GrowStructure(cogmap, ids_gen)
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

def two_hists(sample1, sample2, label1, label2):
    fig, ax1 = plt.subplots()
    ax1.set_ylabel("Counts")
    ax1.set_xlabel("Energy")

    ax1.hist([sample1, sample2], color=['g', 'r'], label=[label1, label2])
    ax1.legend()
    return fig

if __name__ == '__main__':
    logger = HtmlLogger("MAIN_TEST")


    # 1. Создание первичных (LUE) правил расстановки событий и разметка ими когнитивных карт:
    lue_rules = create_LUE_rules()
    logger.add_text("LUE-правила связывают пары событий:")
    logger.add_text(lue_rules.print())
    etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps = get_cogmaps_from_rules(lue_rules, class_num=147, contrast_sample_len=40)
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
    ids_gen = StructIdsGenerator()
    exemplar_predictor, structure_predictor = create_exemplar_and_struct_by_events_list(etalon_cogmap, predictor_events, ids_gen)
    exemplar_prediction, structure_prediction = create_exemplar_and_struct_by_events_list(etalon_cogmap, prediction_events, ids_gen)
    logger.add_text("Эталонный экземпляр предиктора:")
    logger.add_fig(exemplar_predictor.show(etalon_pic))
    logger.add_text("Эталонный экземпляр предсказания:")
    logger.add_fig(exemplar_prediction.show(etalon_pic))

    # 4. Идеальная энергия того и того:
    IDEAL_ENERGY_PREDICTOR = exemplar_predictor.get_exemplar_energy(bank_physical_histograms)
    logger.add_text("Энергия идеального экземпляра предиктора = " + str(IDEAL_ENERGY_PREDICTOR))
    IDEAL_ENERGY_PREDICTION = exemplar_prediction.get_exemplar_energy(bank_physical_histograms)
    logger.add_text("Энергия идеального экземпляра предискауемого = " + str(IDEAL_ENERGY_PREDICTION))
    logger.add_line_big()

    # 5. Безусловная выборка предсказуемого

    unconditional_prediction_sample = unconditional_sample(structure_prediction, contrast_cogmaps + train_cogmaps, bank_physical_histograms,
                                         sample_size=200)
    fig = visualise_sample(unconditional_prediction_sample, range=[ENERGY_OF_NON_FOUND, IDEAL_ENERGY_PREDICTION], n_bins=7)
    logger.add_text("Безусловная выборка предсказуемого на train + contrast:")
    logger.add_text(str(unconditional_prediction_sample))
    logger.add_fig(fig)
    logger.add_line_little()

    # 6. Условная выборка предсказуемого
    cond_rec = ConditionalRecogniser(exemplar_predictor, exemplar_prediction)
    energy_sample_predictor, conditional_prediction_sample = conditional_sample(cond_rec, structure_predictor,
                                                                           train_cogmaps,
                                                                           bank_physical_histograms)
    logger.add_text("Условная выборка предсказуемого TRAIN:")
    logger.add_text(str(conditional_prediction_sample))
    fig = visualise_sample(conditional_prediction_sample, range=[ENERGY_OF_NON_FOUND, IDEAL_ENERGY_PREDICTION],
                           n_bins=7)
    logger.add_fig(fig)
    logger.add_line_little()

    # 6. Сравнение условной и безусловной выборок предсказуемого:
    p_value = get_p_value_for_two_samples(unconditional_prediction_sample, conditional_prediction_sample)
    logger.add_text("Сравнение условной и безусловной выборок предсказуемого:")
    logger.add_text("p_value = "+ str(p_value))
    fig = two_hists(unconditional_prediction_sample, conditional_prediction_sample, "unconditional", "conditional")
    logger.add_fig(fig)
    logger.add_line_little()

    # 7. Итоговый классификатор:
    merged = Merged(exemplar_predictor, exemplar_prediction, bank_physical_histograms)

    logger.add_text("Итоговый классификатор:")
    fig, ax = plt.subplots()
    merged.show_on_cogmap(etalon_cogmap, etalon_pic, ax)
    logger.add_fig(fig)



    fig, energies_true, energies_contrast = merged.visualise(train_cogmaps, contrast_cogmaps)
    logger.add_fig(fig)
    p_value = get_p_value_for_two_samples(energies_true, energies_contrast)
    logger.add_text("p_value = " + str(p_value))
    logger.add_line_little()
    logger.add_text("Срабатывание смерженной структуры на трейне:")
    fig = merged.show_on_cogmaps(train_cogmaps, train_pics)
    logger.add_fig(fig)


    logger.close()


