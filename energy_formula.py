

def get_energy(probabilities_list):
    energy = 0
    for probability in probabilities_list:
        energy += (1 - probability)
    return energy
