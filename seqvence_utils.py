from common_utils import *

from random import choice

def try_grow_seq_of_points_unknown_u(start_point, binary_img, max_rad):
    if sense_1(start_point, binary_img) is False:
        return []
    second_p = find_nearest_1(start_point, binary_img, max_rad)
    if second_p is None:
        return []
    u = Point(second_p.x - start_point.x, second_p.y - start_point.y)
    return try_qrow_seq_of_points_with_u(start_point, binary_img, u, max_rad)

def try_qrow_seq_of_points_with_u(start_point, binary_img, u, max_rad):
    if sense_1(start_point, binary_img) is False:
        return []
    seq_of_points = [start_point]
    last_point = start_point
    while True:
        next_expected_point = Point(x=last_point.x + u.x, y=last_point.y + u.y)
        next_real_point = find_nearest_1_with_exclusions(next_expected_point, binary_img, max_rad, exclusions=seq_of_points)
        if next_real_point is None:
            break
        seq_of_points.append(next_real_point)
        last_point = next_real_point
    # обратный проход
    u = get_backward_dir(u)
    last_point = seq_of_points[0]
    while True:
        next_expected_point = Point(x=last_point.x + u.x, y=last_point.y + u.y)
        next_real_point = find_nearest_1_with_exclusions(next_expected_point, binary_img, max_rad, exclusions=seq_of_points)
        if next_real_point is None:
            break
        seq_of_points.insert(0, next_real_point)
        last_point = next_real_point
    return seq_of_points


def remove_dubles(seqs_list):
    indexes_to_remove=set()
    for i in range(len(seqs_list)):
        for j in range(i+1, len(seqs_list)):
            if are_dubles(seqs_list[i], seqs_list[j]):
                indexes_to_remove.add(i)
                break
    new_seq_list = []
    for i in range(len(seqs_list)):
        if i not in indexes_to_remove:
            new_seq_list.append(seqs_list[i])
    seqs_list = new_seq_list

def are_dubles(seq1, seq2):
    num_of_common_elements = 0
    for elt1 in seq1:
        for elt2 in seq2:
            if elt1 == elt2:
                num_of_common_elements +=1
                break
    max_len = max(len(seq1), len(seq2))
    diff = max_len - num_of_common_elements
    if num_of_common_elements>diff: # общего больше, чем разного (эвристика)
        print("duble found")
        return True
    return False











