from structure_description import *
from bank_of_physical_samples import *
from common_utils import Point

class StructureExemplar:
    def __init__(self, struct_description):
        self.events_coords = {}# event_id:coord
        self.masses = {} # mass_id: mass
        self.us = {} # u_id: u

        self.struct_rescription = struct_description # какой структуры это экземпляр

    #  заполнение экземпляра данными по мере распознавания произво-
    #  дится через эти два метода:                   ----------
    def add_event_data(self, event_id, coord, mass, mass_id):
        self.events_coords[event_id]=coord
        self.masses[mass_id]=mass

    def add_u_data(self, u_id, u):
        self.us[u_id]=u
    # --------------------------------------------------------------

    def _get_probabilities_for_all_relaxable_params(self, bank_physical_histograms):
        result = {}  # param_id : probability
        # из struct_rescription вытаскиваем эталонные значения релаксируемых параметров
        # из экземпляра реальные их значения

        # заполняем данные по массам
        for mass_id, real_mass in self.masses.items():
            LUE_event_id, etalon_mass = self.struct_rescription.get_LUE_id_and_mass_by_mass_id(mass_id)
            dm = abs(real_mass-etalon_mass)
            probability = bank_physical_histograms.get_probability_of_mass_of_event(etalon_mass, dm, LUE_event_id)
            result[mass_id] = probability

        # заполняем данные по смещениям
        for u_id, real_u in self.us.items():
            LUE_event_id = self.struct_rescription.get_LUE_id_of_end_of_u(u_id)
            etalon_u = self.struct_rescription.get_u(u_id)
            du=Point(x=real_u.x-etalon_u.x, y=real_u.y-etalon_u.y)
            probability = bank_physical_histograms.get_probability_of_du_of_event(du, LUE_event_id)
            result[u_id] = probability
        return result

    def get_exemplar_energy(self, bank_physical_histograms):
        params_probabilities = self._get_probabilities_for_all_relaxable_params( bank_physical_histograms)
        energy = 0
        for param_id, propbability in params_probabilities.items():
            energy+=1-propbability
        return energy

