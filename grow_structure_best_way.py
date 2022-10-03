from cogmap import *
from bank_of_physical_samples import BankOfPhysicalSamples, MAX_RAD
from energy_formula import get_energy
from logger import HtmlLogger
from trainig_utils import *

# отранжровать собыия на данной когнитивной карте, начиная с максимально редких
def get_rarest_events_in_cogmap(cogmap, bank_of_physical_samples):
    DU=1
    DM=1
    all_local_event_ids = cogmap.get_all_local_event_ids()
    events_energies = {}
    for local_event_id in all_local_event_ids:
        _, LUEid, mass = cogmap.get_event_data(local_event_id)
        prob_mass = bank_of_physical_samples.get_probability_of_mass_of_event(mass, DM, LUEid)
        prob_du = bank_of_physical_samples.get_probability_of_du_of_event(DU, LUEid)
        energy = get_energy([prob_mass, prob_du])
        events_energies[local_event_id] = energy
    sorted_events = dict(sorted(events_energies.items(), key=lambda item: item[1], reverse=True))
    return sorted_events


class CleverGrower:
    def __int__(self):
        pass


def main(name, class_num):
    logger = HtmlLogger("CLEVER_GROW"+name)

    # 1. Создание первичных (LUE) правил расстановки событий и разметка ими когнитивных карт:
    lue_rules = create_LUE_rules()
    logger.add_text("LUE-правила связывают пары событий:")
    logger.add_text(lue_rules.print())
    etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps, contrast_pics = get_cogmaps_from_rules(
        lue_rules, class_num=class_num, contrast_sample_len=40)
    logger.add_text("Эталонная когнитивная карта:")
    logger.add_text(etalon_cogmap.print())
    logger.add_fig(etalon_cogmap.draw(etalon_pic))
    logger.add_line_big()

