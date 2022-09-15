from structure_description import *
import matplotlib.patches as mpatches
from bank_of_physical_samples import BankOfPhysicalSamples, MAX_RAD
from common_utils import Point, my_dist

import matplotlib.pyplot as plt

class StructureExemplar:
    def __init__(self, struct_description):
        self.events_coords = {}# event_id:coord
        self.events_masses = {} # event_id: mass
        self.dus = {} # u_id: du

        self.struct_rescription = struct_description # какой структуры это экземпляр

    def set_event_data(self, event_id, real_coord, real_mass, incoming_u_error):
        self.events_coords[event_id]=real_coord
        self.events_masses[event_id]=real_mass
        incoming_u_id = self.struct_rescription.get_incoming_u_id(event_id)
        self.dus[incoming_u_id]=incoming_u_error

    def get_mass_of_event(self, event_id):
        return self.events_masses[event_id]

    def get_LUE_of_event(self, event_id):
        lue_id, _ = self.struct_rescription.get_event_LUE_and_mass(event_id)
        return lue_id

    def _get_probabilities_for_all_relaxable_params(self, bank_physical_histograms):
        result = {}  # param_id : probability
        # заполняем данные по массам
        for event_id, real_mass in self.events_masses.items():
            LUE_event_id, etalon_mass = self.struct_rescription.get_event_LUE_and_mass(event_id)
            dm = abs(real_mass-etalon_mass)
            probability = bank_physical_histograms.get_probability_of_mass_of_event(etalon_mass, dm, LUE_event_id)
            #result[event_id] = probability

        # заполняем данные по смещениям
        for u_id, du in self.dus.items():
            LUE_event_id = self.struct_rescription.get_LUE_id_of_end_of_u(u_id)
            probability = bank_physical_histograms.get_probability_of_du_of_event(du, LUE_event_id)
            result[u_id] = probability

        return result


    def get_exemplar_energy(self, bank_physical_histograms):
        params_probabilities = self._get_probabilities_for_all_relaxable_params(bank_physical_histograms)
        energy = 0
        for _, propbability in params_probabilities.items():
            energy+=(1-propbability)

        return energy

    def find_event_nearest_to_point(self, point):
        best_id = None
        best_point = None
        best_dist =None
        for event_id , coord in self.events_coords.items():
            if best_id is None:
                best_id = event_id
                best_point = coord
                best_dist = my_dist(point,coord)
                continue
            current_dist= my_dist(point,coord)
            if current_dist < best_dist:
                best_id = event_id
                best_point = coord
                best_dist = current_dist
        return best_id ,best_point

    def show(self, back_pic_binary):
        fig, ax= plt.subplots()
        fig.title="Exemplar : showd id in struct"
        cm = plt.get_cmap('gray')
        ax.imshow(back_pic_binary, cmap=cm, vmin=0, vmax=1)

        for event_id, coord in self.events_coords.items():
            marker = '$' + str(event_id) + '$'
            annotation = "(mass=" + str(self.get_mass_of_event(event_id))+ ", LUE="+str(self.get_LUE_of_event(event_id))+")"
            ax.scatter(coord.x, coord.y, c='green', marker=marker, alpha=0.8, s=200)
            ax.annotate(annotation, (coord.x, coord.y), color='blue', xytext=(20,15), textcoords='offset points',
                         ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.6),
                         arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.95',  color='b'))

            prev_event_id = self.struct_rescription.get_prev_event(event_id)
            if prev_event_id is not None:
                prev_event_coord = self.get_coord_of_event(prev_event_id)
                arrow = mpatches.FancyArrowPatch((prev_event_coord.x, prev_event_coord.y), (coord.x, coord.y),
                                                 mutation_scale=10)
                ax.add_patch(arrow)

        return fig

    def get_coord_of_event(self, event_id):
        return self.events_coords[event_id]