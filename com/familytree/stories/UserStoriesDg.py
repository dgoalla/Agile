
from datetime import datetime

from com.familytree.TreeError import TreeError
from com.familytree.TreeUtils import TreeUtils
from com.familytree.TreeLine import TreeLine

class UserStoriesDg:

    FILE_PATH = './com/familytree/data/us05&07.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'

    def us07(self, file_path=None):
        """
        returns a list of objects with age greater than or equal to 150
        """
        file_path = file_path if file_path else UserStoriesDg.FILE_PATH
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesDg.INDI_TAG)
        indi_list_us07 = []
        for indi in indi_list:
            if indi.get_age() >= 150:
                warn_msg = f'Age is greater than or equal to 150, Age: {indi.get_age()}'
                indi.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US07', indi.id, warn_msg)
                indi_list_us07.append(indi)
                continue
        # if indi_list_us07:
            #TreeLine().tabulate(processed_tree)
            # TreeUtils.print_report("US07 Less then 150 years old", indi_list_us07)
        return indi_list_us07

    def us05(self, file_path=None):
        """
        returns a list of objects whose divorse date is before death date
        """
        file_path = file_path if file_path else UserStoriesDg.FILE_PATH
        processed_tree = TreeLine().process_data(file_path)
        fam_list = processed_tree.get_sorted_list(UserStoriesDg.FAM_TAG)
        fam_list_us05 = []
        for fam in fam_list:
            marr_date = fam.get_marr_date()
            hus_death_date = processed_tree.get(fam.husb).get_death_date() if processed_tree.get(fam.husb) else None
            wife_death_date = processed_tree.get(fam.wife).get_death_date() if processed_tree.get(fam.wife) else None
            if marr_date:
                warn_msg = f'Marriage should occur before death of spouse {processed_tree.get(fam.husb).name}, {processed_tree.get(fam.wife).name}'
                if hus_death_date and wife_death_date:
                    if wife_death_date < marr_date and hus_death_date < marr_date:
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US07', fam.id, warn_msg)
                        fam_list_us05.append(fam)
                elif hus_death_date or wife_death_date:
                    if hus_death_date and hus_death_date < marr_date:
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US07', fam.id, warn_msg)
                        fam_list_us05.append(fam)
                    elif wife_death_date and wife_death_date < marr_date:
                        fam.err = TreeError(TreeError.TYPE_ERROR, TreeError.ON_INDI, 'US07', fam.id, warn_msg)
                        fam_list_us05.append(fam)
                    else:
                        continue
                else:
                    pass
        # if fam_list_us05:
            #TreeLine().tabulate(processed_tree)
            # TreeUtils.print_report("US05 Marriage should occur before death of either spouses", fam_list_us05)
        return fam_list_us05

    def get_id_list(self, obj_list):
        """ return the individual or family id's """

        id_list = []
        if obj_list:
            for obj in obj_list:
                id_list.append(obj.id)
        return id_list
