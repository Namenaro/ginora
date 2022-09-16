from cogmap import *
from structure_description import *
from common_utils import Point
from structure_exemplar import *
from dataset_getter import get_all_for_start
from logger import HtmlLogger
from grow_structure import *
from main_constants import *

from copy import deepcopy


def find_exemplar_from_point(cogmap, struct, point):
    new_cogmap = deepcopy(cogmap) # мы будем удалять учтенныe события, а исходную карту повредить нельзя
    exemplar = StructureExemplar(struct)

    for event_id in struct.events_order_during_recognition:
        LUE_id = struct.get_event_LUE(event_id)

        if struct.is_first_event(event_id):
            point_of_prev_event = point
            _,  incoming_u, expected_mass = struct.get_event_data(event_id)
            if incoming_u is None:
                incoming_u = Point(0, 0)
        else:
            prev_event_id, incoming_u, expected_mass = struct.get_event_data(event_id)
            point_of_prev_event = exemplar.get_coord_of_event(prev_event_id)

        predicted_point_of_this_event = Point(point_of_prev_event.x + incoming_u.x, point_of_prev_event.y + incoming_u.y )
        id_in_cogmap, real_coord, real_mass = new_cogmap.find_event_in_cogmap(predicted_point_of_this_event, LUE_id, expected_mass)
        if id_in_cogmap is None:
            return None
        new_cogmap.delete_event(id_in_cogmap)
        incoming_u_error = Point(real_coord.x - predicted_point_of_this_event.x, real_coord.y - predicted_point_of_this_event.y)
        exemplar.set_event_data(event_id, real_coord, real_mass, incoming_u_error)

    return exemplar

def find_best_exemplar_in_cogmap(cogmap, struct, bank_of_physical_samples):
    exemplars = get_all_exemplars_of_struct_in_cogmap(cogmap, struct)
    if len(exemplars)==0:
        return None, ENERGY_OF_NON_FOUND
    best_exemplar= exemplars[0]
    best_energy = best_exemplar.get_exemplar_energy(bank_of_physical_samples)
    for i in range(1, len(exemplars)):
        energy = exemplars[i].get_exemplar_energy(bank_of_physical_samples)
        if energy>best_energy:
            best_energy = energy
            best_exemplar = exemplars[i]
    return best_exemplar, best_energy

def get_all_exemplars_of_struct_in_cogmap(cogmap, struct): # эта функция не реализует полный перебор, а слабую жадную эвристику. Полный тоже сделать не сложно.
    exemplars = []
    first_LUE_to_find = struct.get_first_event_LUE()
    start_points = cogmap.get_all_points_for_LUE(first_LUE_to_find)
    for start_point in start_points:
        exemplar = find_exemplar_from_point(cogmap, struct, start_point)
        if exemplar is not None:
            exemplars.append(exemplar)
    return exemplars

def visualise_struct_recogmition_on_several_cogmaps(struct, cogmaps, pics, bank_of_physical_samples, logger, energy_range):
    for i in range(len(pics)):
        best_exemplar, best_energy = find_best_exemplar_in_cogmap(cogmaps[i], struct, bank_of_physical_samples)
        logger.add_text("BEST_EXEMPLAR_IN_COGMAP:")
        logger.add_text("BEST energy = "+str(best_energy))
        fig = best_exemplar.show(pics[i])
        logger.add_fig(fig)
        logger.add_text("energies in cogmap:")
        energies = []
        exemplars = get_all_exemplars_of_struct_in_cogmap(cogmaps[i], struct)
        for exemplar in exemplars:
            energies.append(exemplar.get_exemplar_energy(bank_of_physical_samples))
        fig, ax = plt.subplots()
        ax.plot(energies, 'bo')
        plt.ylim(energy_range)
        logger.add_fig(fig)
        logger.add_line_little()
        logger.add_text("all exemplars in this cogmap:")
        for j in range(len(exemplars)):
            exemplar = exemplars[j]
            logger.add_text("energy=" +str(energies[j]))
            fig = exemplar.show(pics[i])
            logger.add_fig(fig)

if __name__ == '__main__':
    struct_size = 3
    logger = HtmlLogger("recogn_" + str(struct_size))
    num_of_test_structs = 1

    etalon_cogmap, etalon_pic, train_cogmaps, train_pics, contrast_cogmaps = get_all_for_start(class_num=147)
    bank_physical_histograms = BankOfPhysicalSamples(contrast_cogmaps + train_cogmaps, cycles=200)
    for j in range(num_of_test_structs):
        logger.add_line_big()
        logger.add_text("Ideal exemplar:")
        struct, ideal_exemplar = create_random_structure(etalon_cogmap, struct_size)
        fig = ideal_exemplar.show(etalon_pic)
        max_energy = ideal_exemplar.get_exemplar_energy(bank_physical_histograms)
        logger.add_text("energy MAX= "+ str(max_energy))
        logger.add_fig(fig)
        logger.add_line_little()


        logger.add_text("visualise_struct_recogmition_on_several_cogmaps:")
        n_cogmaps=5
        visualise_struct_recogmition_on_several_cogmaps(struct, train_cogmaps[:n_cogmaps],train_pics[:n_cogmaps], bank_physical_histograms, logger, [-1, max_energy])
    logger.close()



