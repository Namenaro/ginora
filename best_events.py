from cogmap import *
from bank_of_physical_samples import BankOfPhysicalSamples, MAX_RAD
from energy_formula import get_energy

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
    sorted_events = dict(sorted(events_energies.items(), key=lambda item: item[1]))
    return sorted_events
