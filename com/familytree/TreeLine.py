from prettytable import PrettyTable

from com.familytree.Individual import Individual
from com.familytree.Family import Family


class TreeLine:

    zero_tags = ["FAM", "INDI", "HEAD", "TRLR", "NOTE"]
    one_tags = ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"]
    two_tags = ['DATE']
    allowed_tags_on_level = {
        '0': zero_tags,
        '1': one_tags,
        '2': two_tags
    }
    all_tags = zero_tags + one_tags + two_tags

    def __init__(self, input_line):
        split_text = input_line.strip().split(' ', maxsplit=2)
        # print(split_text)
        self.level = split_text[0]
        self.tag_name = self.extract_tag_name(input_line)
        self.arguments = self.extract_arguments(input_line)
        self.is_valid = 'Y' if self.is_valid(input_line) else 'N'

    def is_valid(self, input_line):
        if not input_line:
            return False
        if len(input_line.strip()) == 0:
            return False
        split_text = self.split_to_list(input_line)
        if len(split_text) < 2:
            return False
        tag_name = self.get_tag_name()
        level = self.get_level()
        return True if tag_name in self.allowed_tags_on_level.get(level, 'False') else False

    def extract_arguments(self, input_line):
        if not input_line:
            return ''
        if len(input_line) == 0:
            return ''
        split_text = self.split_to_list(input_line)
        tag_name = self.get_tag_name()
        if len(split_text) < 3:
            return ''
        if tag_name in ['FAM', 'INDI']:
            return split_text[1]
        return split_text[2]

    def get_level(self):
        return self.level

    def get_tag_name(self):
        return self.tag_name

    def get_arguments(self):
        return self.arguments

    def split_to_list(self, input_line):
        if not input_line:
            return
        return input_line.strip().split(' ', maxsplit=2)

    def extract_tag_name(self, input_line):
        if not input_line.strip():
            return ''
        split_text = self.split_to_list(input_line)
        # print(split_text)
        if self.get_level() == '0':
            if len(split_text) > 2:
                if split_text[2] in ['FAM', 'INDI']:
                    return split_text[2]

        return split_text[1] if split_text[1] in ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE'] else ''

    def print_line(self, input_line):
        if not input_line:
            return
        if len(input_line.strip()) == 0:
            return
        print(f'--> {input_line.strip()}')

    def print_line_info(self, input_line):
        if not input_line:
            return
        if len(input_line.strip()) == 0:
            return
        info_string = self.generate_info_string(input_line)
        print(info_string)

    def generate_info_string(self, input_line):
        if not input_line:
            return ''
        if len(input_line.strip()) == 0:
            return ''
        return f'<-- {self.level}|{self.tag_name}|{self.is_valid}|{self.arguments}'

    def get_tags_of_type(self, tag_name):
        if tag_name and treeline_list:
            tag_list = []
            for treeline in treeline_list:
                if treeline.get_tag_name() == tag_name:
                    tag_list.append(treeline)
            return tag_list
        return

    def print_indi(self):
        for treeline in treeline_list:
            if treeline.get_tag_name() == 'INDI':
                print('start to create Individual object')

    @staticmethod
    def process_data(file_path):
        file = open(file_path, 'r')
        for line in file:
            tl = TreeLine(line)
            # tl.print_line(line)
            # tl.print_line_info(line)
            treeline_list.append(tl)

    @staticmethod
    def generate_indi_objects():
        if treeline_list:
            curr_zero_tag = None
            curr_one_tag = None
            curr_obj_map = {}
            processed_obj_map = {}
            for treeline in treeline_list:
                # print(f'reading treeline: {treeline.get_tag_name()}|{treeline.get_arguments()}|{treeline.is_valid}')
                # if the treeline is not valid, skip to the next treeline
                if treeline.is_valid == 'N':
                    # print('treeline not valid, moving to next')
                    continue

                if treeline.get_level() == '0':
                    if curr_zero_tag in curr_obj_map:
                        processed_obj = curr_obj_map[curr_zero_tag]
                        processed_obj_map[processed_obj.id] = processed_obj
                    curr_zero_tag = treeline.get_tag_name()
                    if curr_zero_tag == 'INDI':
                        curr_indi_object = Individual(treeline.get_arguments())
                        curr_obj_map[curr_zero_tag] = curr_indi_object
                    if curr_zero_tag == 'FAM':
                        curr_fam_object = Family(treeline.get_arguments())
                        curr_obj_map[curr_zero_tag] = curr_fam_object

                if treeline.get_level() == '1':
                    if not curr_zero_tag:
                        continue
                    curr_one_tag = treeline.get_tag_name()
                    # if treeline.get_tag_name() not in ['BIRT', 'DEAT', 'MARR']:
                    curr_obj_map[curr_zero_tag].set_attr(treeline.get_tag_name(), treeline)

                if treeline.get_level() == '2':
                    if not curr_one_tag:
                        continue
                    curr_two_tag = treeline.get_tag_name()
                    curr_obj_map[curr_zero_tag].set_attr(curr_one_tag, treeline)

            if curr_zero_tag in ['INDI', 'FAM']:
                if curr_obj_map[curr_zero_tag]:
                    processed_obj = curr_obj_map[curr_zero_tag]
                    processed_obj_map[processed_obj.id] = processed_obj

        return processed_obj_map

    @staticmethod
    def table_printer(table_name, heading_list):
        x = PrettyTable(heading_list)
        x.align[0] = "1"
        x.padding_width = 1
        x.table_name = table_name
        return x

    @staticmethod
    def print_table(heading_list, data_list):
        x = PrettyTable(heading_list)
        x.align["ID"] = "1"
        x.padding_width = 1
        for data in data_list:
            x.add_row(data)
        print(x)

    @staticmethod
    def process_for_pretty_table(type, type_obj, processed_obj_map):
        if type == 'FAM':
            family = processed_obj_map[type_obj.id]
            husb_id = family.husb
            wife_id = family.wife
            if wife_id in processed_map:
                wife_indi = processed_map[wife_id]
                type_obj.wife_name = wife_indi.name
            else:
                type_obj.wife_name = 'NA'

            if husb_id in processed_map:
                husb_indi = processed_map[husb_id]
                type_obj.husb_name = husb_indi.name
            else:
                type_obj.husb_name = 'NA'

        if type == 'INDI':
            indi = processed_map[type_obj.id]
            type_obj.age = indi.get_age()
            type_obj.alive = indi.get_alive()

    @staticmethod
    def print_fam_table(fam_list, processed_map):
        heading_list = ["ID", "Married", "Divorced", "Husband ID", "Husband Namw", "Wife ID", "Wife Name", "Children"]
        table_printer = TreeLine.table_printer("Family", heading_list)
        for fam in fam_list:
            table_printer.add_row([fam.id, fam.marr, fam.div, fam.husb, "husby", fam.wife, "wifey", fam.chil])

        print(f'Families\n{table_printer}')

    @staticmethod
    def print_indi_table(indi_list, processed_map):
        heading_list = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
        table_printer = TreeLine.table_printer("Indi", heading_list)
        for indi in indi_list:
            TreeLine.process_for_pretty_table('INDI', indi, processed_map)
            table_printer.add_row([indi.id, indi.name, indi.sex, indi.birt, indi.age, indi.alive, indi.deat, indi.famc, indi.fams])
        print(f'Individuals\n{table_printer}')

    @staticmethod
    def pretty_print_table(table_name, data_list, processed_map):
        if table_name == 'INDI':
            TreeLine.print_indi_table(data_list, processed_map)
        if table_name == 'FAM':
            TreeLine.print_fam_table(data_list, processed_map)


treeline_list = []
if __name__ == '__main__':
    TreeLine.process_data('./data/Familytree_test_file.ged')
    processed_map = TreeLine.generate_indi_objects()
    indi_list = []
    fam_list = []
    for key in processed_map:
        if processed_map[key].tag_name == 'INDI':
            indi_list.append(processed_map[key])
        else:
            fam_list.append(processed_map[key])

    TreeLine.pretty_print_table('INDI', indi_list, processed_map)
    TreeLine.pretty_print_table('FAM', fam_list, processed_map)
