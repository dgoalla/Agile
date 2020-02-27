from datetime import datetime, timedelta
from TreeLine import TreeLine
import calendar

class UserStoriesAm:

    FILE_PATH = '../data/Family_US02_US06.ged'
    INDI_TAG = 'INDI'
    FAM_TAG = 'FAM'
    
    def us02(self):
        """return a list of objects whose birth date is before after their marriage date """
        file_path = './com/familytree/data/Family_US02_US06.ged'
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesAm.INDI_TAG)
        indi_list_us02_fail = []
        for indi in indi_list:
            birth_date = indi.get_birth_date()
            for spouse in indi.fams:
                marriage_date = processed_tree.get(spouse).get_marr_date() if processed_tree.get(spouse) else None
                if marriage_date and birth_date > marriage_date:
                    indi_list_us02_fail.append(indi)
                    print(f"birth after marriage - {processed_tree.get(indi.id)}")
                    continue
        return indi_list_us02_fail 
    
    def us06(self):
        """ return a list of objects whose birth date is before after their marriage date """
        file_path = './com/familytree/data/Family_US02_US06.ged'
        processed_tree = TreeLine().process_data(file_path)
        indi_list = processed_tree.get_sorted_list(UserStoriesAm.INDI_TAG)
        fam_list = processed_tree.get_sorted_list(UserStoriesAm.FAM_TAG)
        indi_list_us06_fail = []
        for fam in fam_list:
            husband_death_date = processed_tree.get(fam.husb).get_death_date() if processed_tree.get(fam.husb) else None
            wife_death_date = processed_tree.get(fam.wife).get_death_date() if processed_tree.get(fam.wife) else None
            divorce_date = fam.get_div_date() 
            if divorce_date:
                if husband_death_date and wife_death_date:
                    if divorce_date > husband_death_date and divorce_date > wife_death_date:
                        print(f"death occurs before divorse both people - {processed_tree.get(fam.husb).name}, {processed_tree.get(fam.wife).name} ")
                        indi_list_us06_fail.append(fam)
                elif husband_death_date or wife_death_date:
                    if husband_death_date and divorce_date > husband_death_date:
                        print(f"death occurs before divorse when husb dead - {processed_tree.get(fam.husb).name}")
                        indi_list_us06_fail.append(fam)
                    if wife_death_date and divorce_date > wife_death_date:
                        print(f"death occurs before divorse when wife dead - {processed_tree.get(fam.wife).name} ")
                        indi_list_us06_fail.append(fam)
                else:
                    continue                                      
        return indi_list_us06_fail 

if __name__ == '__main__':
    usam = UserStoriesAm()
    #usam.us06()
    usam.us02()
    
            
        