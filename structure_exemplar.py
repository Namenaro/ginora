from structure_description import *

class StructureExemplar:
    def __init__(self, struct_description):
        self.events_coords = {}# event_id:coord
        self.masses = {} # mass_id: mass
        self.us = {} # u_id: u

        self.struct_rescription = struct_description # какой структуры это экземпляр

    #  заполнение данными по мере распознавания----------
    def add_event_data(self, event_id, coord, mass, mass_id):
        self.events_coords[event_id]=coord
        self.masses[mass_id]=mass

    def add_u_data(self, u_id, u):
        self.us[u_id]=u

    # ---------------------------------------------------

    def _get_probabilities_for_all_relaxable_params(self, bank_physical_histograms):
        pass


