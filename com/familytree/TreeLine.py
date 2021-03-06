from datetime import datetime

import com
from com.familytree.Individual import Individual
from com.familytree.Family import Family
# from com.familytree.Tree import Tree
from com.familytree.TreeUtils import TreeUtils


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
    logger = TreeUtils.get_logger()

    def __init__(self, input_line=None, line_num=-1, id=-1, src_file=None):
        """
        TreeLine object takes a line of gedcome file as input like "0 @I1@ INDI"
        the constructor extracts the level, tag name and arguments from the line
        an is_valid flag is set on the current object based on whether the line is valid
        :param input_line: the line from gedcom file which will be translated into TreeLine object
        """
        if input_line:
            split_text = input_line.strip().split(' ', maxsplit=2)
            self.level = split_text[0]
            self.tag_name = self.extract_tag_name(input_line)
            self.arguments = self.extract_arguments(input_line)
            self.is_valid = self.is_valid_tags(input_line)
            self.src_file = src_file
            self.id = id
            self.line_num = line_num

    def __str__(self):
        """
        :return: a string representation of values contained inside the treeline object
        """
        return f'<-- {self.level}|{self.tag_name}|{"Y" if self.is_valid else "N"}|{self.arguments}'

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

    def is_valid_tags(self, input_line):
        """
        validates whether the input_line in gedcom file is valid or not
        :param input_line: the line that has to be validated
        :return: true if the line is valid, false otherwise
        """
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
        """
        extracts the argument text from input_line
        :param input_line: the line as string which contains the arguments
        :return: the arguments in the input line if found or an empty string if not found
        """
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

    def extract_tag_name(self, input_line):
        """
        extracts the tag name from input_line
        :param input_line: the line containing tag name
        :return: the tag name from the input line if found or
        """
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
        """
        prints the input_line as it is from the gedcom
        :param input_line: the line to be printed
        :return: a string if line found, None otherwise
        """
        if not input_line:
            return
        if len(input_line.strip()) == 0:
            return
        print(f'--> {input_line.strip()}')

    def print_line_info(self, input_line):
        """
        prints the input line from the TreeLine object (self)
        :param input_line: the line to be printed
        :return: a formatted string if input_line not empty or None otherwise
        """
        if not input_line:
            return
        if len(input_line.strip()) == 0:
            return
        print(self)

    def get_tags_of_type(self, tag_name):
        """
        internal method used to segregate all treeline objects of a particular type
        :param tag_name: the type of tag requested (to be passed as 'FAM' or 'INDI' tags
        :return: a list of treeline objects of the type tag_name, None otherwise
        """
        if tag_name and treeline_list:
            tag_list = []
            for treeline in treeline_list:
                if treeline.get_tag_name() == tag_name:
                    tag_list.append(treeline)
            return tag_list
        return

    def print_indi(self):
        """
        prints all the treeline objects with tag name INDI
        :return:
        """
        for treeline in treeline_list:
            if treeline.get_tag_name() == 'INDI':
                print('start to create Individual object')

    # keeping this only as a legacy method. everyone knows this as the method to generate the family tree
    def process_data(self, file_path):
        """
        opens the gedcom file, reads each line, creates treeline object for each line
        and returns a list of all treeline objects
        :param file_path: location of gedcom file to be used as input
        :return: list of all treeline objects created from the supplied gedcom file
        """
        return com.familytree.Tree.Tree().grow(file_path)

    # def process_for_pretty_table(self, type, type_obj, processed_tree):
    #     """
    #     helper method to call the corresponding table processing method for FAM or INDI
    #     :param type: string denoting the type of object to be printed
    #     :param type_obj: the actual data object to be printed
    #     :param processed_tree: the Tree object containing the complete family tree
    #     :return: not required at the moment, doesn't get used right now
    #     """
    #     if type == 'FAM':
    #         return self.process_fam_for_table(type_obj, processed_tree)
    #     if type == 'INDI':
    #         return self.process_indi_for_table(type_obj, processed_tree)

    # def process_fam_for_table(self, type_obj, family_tree):
    #     """
    #     helper method to process Family object for displaying in table
    #     :param type_obj: the actual data object to be printed
    #     :param family_tree: the Tree object containing the complete family tree
    #     :return: not required at the moment
    #     """
    #     family = family_tree.get(type_obj.id)
    #     type_obj.husb_id_disp = family.husb if family.husb else 'NA'
    #     type_obj.wife_id_disp = family.wife if family.wife else 'NA'
    #     type_obj.husb_name = family_tree.get(family.husb).name if family_tree.contains(family.husb) else 'NA'
    #     type_obj.wife_name = family_tree.get(family.wife).name if family_tree.contains(family.wife) else 'NA'
    #     type_obj.marr_disp = datetime.strptime(type_obj.marr, Individual.date_format).strftime(TreeUtils.OUTPUT_DATE_FORMAT) if type_obj.marr else 'NA'
    #     type_obj.div_disp = datetime.strptime(type_obj.div, Individual.date_format).strftime(TreeUtils.OUTPUT_DATE_FORMAT) if type_obj.div else 'NA'
    #     type_obj.chil_disp = type_obj.chil if type_obj.chil else 'NA'
    #     # type_obj.marr = type_obj.marr if type_obj.marr else 'NA'
    #     # type_obj.div = type_obj.div if type_obj.div else 'NA'
    #     return type_obj

    # def process_indi_for_table(self, type_obj, processed_tree):
    #     """
    #     helper method to process Individual object for displaying in table
    #     :param type_obj: the actual data object to be printed
    #     :param processed_tree: the Tree object containing the complete family tree
    #     :return: not required at the moment
    #     """
    #     if not processed_tree.get(type_obj.id):
    #         return type_obj
    #     indi = processed_tree.get(type_obj.id)
    #     type_obj.age_disp = indi.get_age() if indi.get_age() else 'NA'
    #     type_obj.alive_disp = indi.is_alive()
    #     type_obj.name_disp = type_obj.name if type_obj.name else 'NA'
    #     type_obj.sex_disp = type_obj.sex if type_obj.sex else 'NA'
    #     type_obj.deat_disp = datetime.strptime(type_obj.deat, Individual.date_format).strftime(TreeUtils.OUTPUT_DATE_FORMAT) if type_obj.deat else 'NA'
    #     type_obj.famc_disp = type_obj.famc if type_obj.famc else 'NA'
    #     type_obj.fams_disp = type_obj.fams if type_obj.fams else 'NA'
    #     type_obj.birt_disp = datetime.strptime(type_obj.birt, Individual.date_format).strftime(TreeUtils.OUTPUT_DATE_FORMAT) if type_obj.birt else 'NA'
    #     return type_obj

    # def print_fam_table(self, fam_list, processed_tree):
    #     """
    #     generates and prints the table printer object and adds all the rows and columns
    #     :param fam_list: list of all Family objects
    #     :param processed_tree: Tree object containing the whole tree
    #     """
    #     heading_list = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
    #     table_printer = TreeUtils.get_table_printer("FAM", heading_list)
    #     for fam in fam_list:
    #         self.process_for_pretty_table('FAM', fam, processed_tree)
    #         table_printer.add_row([fam.id, fam.marr_disp, fam.div_disp, fam.husb_id_disp, fam.husb_name, fam.wife_id_disp, fam.wife_name, fam.chil])
    #
    #     self.logger.error(f'Families\n{table_printer}')
    #     print(f'Families\n{table_printer}')

    # def print_indi_table(self, indi_list, processed_map):
    #     """
    #     generates and prints the table printer object and adds rows and columns to it
    #     :param indi_list: list of all Individual objects
    #     :param processed_map: Tree object containing the whole tree
    #     """
    #     heading_list = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    #     table_printer = TreeUtils.get_table_printer("INDI", heading_list)
    #     for indi in indi_list:
    #         self.process_for_pretty_table('INDI', indi, processed_map)
    #         table_printer.add_row([indi.id, indi.name, indi.sex, indi.birt_disp, indi.age_disp, indi.alive_disp, indi.deat_disp, indi.famc_disp, indi.fams_disp])
    #     self.logger.error(f'People\n{table_printer}')
    #     print(f'People\n{table_printer}')

    # def pretty_print_table(self, table_name, data_list, processed_tree):
    #     """
    #     call the corresponding print method for INDI or FAM
    #     :param table_name: used as name of table
    #     :param data_list: list containing all the data objects
    #     :param processed_tree: Tree object containing the whole family tree
    #     """
    #     if table_name == 'INDI':
    #         self.print_indi_table(data_list, processed_tree)
    #     if table_name == 'FAM':
    #         self.print_fam_table(data_list, processed_tree)

    # def get_sep_obj_list(self, processed_tree):
    #     indi_list = []
    #     fam_list = []
    #     processed_map = processed_tree.get_tree_map()
    #     for key in processed_map:
    #         if processed_map[key].tag_name == 'INDI':
    #             indi_list.append(processed_map[key])
    #         else:
    #             fam_list.append(processed_map[key])
    #
    #     return [indi_list, fam_list]

    # def process_and_print(self, obj_type, processed_tree):
    #     self.pretty_print_table(obj_type, processed_tree.get_sorted_list(obj_type), processed_tree)

    def tabulate(self, processed_tree):
        """
        tabulates the whole tree separated as Individual and Family table
        :param processed_tree: Tree object containing the whole tree
        """
        processed_tree.print()


treeline_list = []
