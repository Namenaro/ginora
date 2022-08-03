from common_utils import *
from seqvence_utils import *
from cogmap import *

from copy import deepcopy

class SeqRule:
    def __init__(self, dx, dy, max_rad, id_gen):
        self.dx = dx
        self.dy = dy
        self.max_rad = max_rad
        self.start_event_id = id_gen.generate_id()
        self.end_event_id = id_gen.generate_id()

    def __str__(self):
        return "dx=" + str(self.dx) + ", dy=" + str(self.dy) + ", max_rad="\
               + str(self.max_rad) + ", start_event_id=" + str(self.start_event_id)\
               + ", end_event_id="+ str(self.end_event_id)

    def apply_to_binary_map(self, binary_map, cogmap_to_fill):
        # собираем все единицы в список и из каждой пытаемся
        # вырастить образец последовательсноти по этому правилу,
        # рассмотренные единицы удаляем из списка,
        # процесс завершаем, когда все единицы рассмотрены.
        min_len = 3
        found_seqs = []
        points_to_process = get_all_1_points(binary_map)
        while True:
            if len(points_to_process)<min_len:
                break
            point = points_to_process[-1]
            seq = try_qrow_seq_of_points_with_u(point, binary_map, Point(self.dx, self.dy), self.max_rad)
            remove_points_from_list(points_to_process, seq)
            if len(seq)>=min_len:
                found_seqs.append(seq)
        remove_dubles(found_seqs)
        self._project_seqs_to_cogmap(found_seqs, cogmap_to_fill)

    def _project_seqs_to_cogmap(self, seqs_list, cogmap_to_fill):
        for seq in seqs_list:
            mass = len(seq)
            start_point = seq[0]
            end_point = seq[-1]
            cogmap_to_fill.register_event(start_point, EventData(mass, self.start_event_id))
            cogmap_to_fill.register_event(end_point, EventData(mass, self.end_event_id))



class LUEcontainer:
    def __init__(self):
        self.dict_rules1 = {} # {rule_id: seq_rule}
        self.dict_rules2 = {} # {rule_id: seq_rule}
        self.dict_events1_to_rules2 = {} # {event1_id : [rule2_id]}
        self.id_gen_rules = IdGen()
        self.id_gen_events = IdGen()

    def add_rule_1(self, dx, dy, max_rad):
        rule_1 = SeqRule(dx, dy, max_rad, self.id_gen_events)
        rule1_id = self.id_gen_rules.generate_id()
        self.dict_rules1[rule1_id] = rule_1
        print("RULE_1 ( "+ str(rule1_id)+")" + str(rule_1))
        return rule1_id

    def add_rule_2(self, dx, dy, max_rad, event1_id):
        rule_2 = SeqRule(dx, dy, max_rad, self.id_gen_events)
        rule2_id = self.id_gen_rules.generate_id()
        self.dict_rules2[rule2_id] = rule_2
        if event1_id not in self.dict_events1_to_rules2.keys():
            self.dict_events1_to_rules2[event1_id]=[]
        self.dict_events1_to_rules2[event1_id].append(rule2_id)
        print("RULE_2 ( "+ str(rule2_id)+")" + str(rule_2))
        return rule2_id

    def _get_rule_id_by_event_id(self, event_id):
        for rule_id, rule in self.dict_rules1.items():
            if rule.start_event_id == event_id or rule.end_event_id == event_id:
                return rule_id

        for rule_id, rule in self.dict_rules2.items():
            if rule.start_event_id == event_id or rule.end_event_id == event_id:
                return rule_id
        print ("ERR: no rule with that event_id...")
        return None

    def _get_rule_by_rule_id(self, rule_id):
        if rule_id in self.dict_rules1.keys():
            return self.dict_rules1[rule_id]
        if rule_id in self.dict_rules2.keys():
            return self.dict_rules2[rule_id]
        print("ERR: no rule with that rule_id...")
        return None

    def apply_rule_to_binary_map(self, binary_map, rule_id, cogmap_to_fill): # для отладочных целей
        rule = self._get_rule_by_rule_id(rule_id)
        rule.apply_to_binary_map(binary_map, cogmap_to_fill)


    def apply_all_to_binary_map(self, binary_map):
        cogmap1 = Cogmap()
        for rule1_id, rule1 in self.dict_rules1.items():
            rule1.apply_to_binary_map(binary_map, cogmap1)

        #cogmap2 = Cogmap()
        for event_id in deepcopy(cogmap1.event_ids_set):
            rules2_ids = self.dict_events1_to_rules2.get(event_id)
            if rules2_ids is None:
                continue
            for rule2_id in rules2_ids:
                rule2 = self.dict_rules2[rule2_id]
                binary_map_for_event = cogmap1.to_binary_map(event_id, binary_map.shape)
                rule2.apply_to_binary_map(binary_map_for_event, cogmap1)
        return cogmap1


if __name__ == '__main__':
    lue_container = LUEcontainer()
    rule1_id = lue_container.add_rule_1(dx=1, dy=0, max_rad=1)
    rule2_id = lue_container.add_rule_2(dx=0, dy=1, max_rad=4, event1_id=0)
    pics, _, _ = get_train_test_contrast(class_num=44)
    binary_map = binarise_img(pics[0])

    # test rule 1:
    #print ("test rule 1:")
    #cogmap_to_fill = Cogmap()
    #lue_container.apply_rule_to_binary_map(binary_map, rule1_id, cogmap_to_fill)
    #cogmap_to_fill.draw(binary_map)

    # test rule 2:
    cogmap =  lue_container.apply_all_to_binary_map(binary_map)
    cogmap.draw(binary_map)
