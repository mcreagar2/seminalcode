import os 
import pandas

class putTogether: 
    def __init__(self, path_to_clean, path_to_columnnames): 
        self.path_to_clean = path_to_clean
        self.path_to_columnNames = path_to_columnnames

    def readinFiles(self): 
        dataframe_hold = []
        for files in os.listdir(self.path_to_clean): 
            school_name = files.split("_")[0]
            school_dict = {
                'school_name' : school_name, 
                'dataframe' : pandas.read_excel(os.path.join(self.path_to_clean, files))}
            dataframe_hold.append(school_dict)
        self.smashTogether(dataframe_hold)

    def smashTogether(self, dataframe_hold): 
        # get column names 
        with open(self.path_to_columnNames) as fp: 
            column_names = [column[:-1] for column in fp]
        # edit or insert missing columns 
        for dataframe in dataframe_hold: 
            for index, column_name in enumerate(column_names): 
                if column_name not in (dataframe['dataframe']).columns.tolist(): 
                    # all exceptions found by hand 
                    ###########################################
                    if (dataframe['school_name'] == "UNL" and column_name == "Start Date"): 
                        (dataframe['dataframe']).rename(columns = {"StartDate" : column_name}, inplace = True)
                    ###########################################
                    elif (dataframe['school_name'] == "UNL" and column_name == "IP Address"): 
                        (dataframe['dataframe']).rename(columns = {"IPAddress" : column_name}, inplace = True)
                    ###########################################
                    elif (dataframe['school_name'] == "UNL" and column_name == "TutoringSource - Selected Choice - Tutoring center at ${e://Field/Site} (please identify the center):"): 
                        (dataframe['dataframe']).rename(columns = {"TutoringSource - Selected Choice - Tutoring center at ${e://Field/Site}&nbsp;(please identify the center):" : column_name}, inplace = True)
                    ###########################################
                    elif (dataframe['school_name'] == "MSU" and column_name == "TutoringSource - Tutoring center at [Field-Site] (please identify the center): - Text"): 
                        (dataframe['dataframe']).rename(columns = {"TutoringSource - Tutoring center at Morgan State University  (please identify the center): - Text" : column_name}, inplace = True)
                    ###########################################
                    elif (dataframe['school_name'] in ["MSU", "OhioState"] and column_name == "NextCourse - Other (please explain) - Text"): 
                        if dataframe['school_name'] == "MSU": 
                            (dataframe['dataframe']).rename(columns = {"NextCourse - Other - Text" : column_name}, inplace = True)
                        else: 
                            (dataframe['dataframe']).rename(columns = {"NextCourse - Other: - Text" : column_name}, inplace = True)
                    ###########################################
                    elif (column_name == "PIPS - I constructively criticize other students ideas during class"): 
                        if (dataframe['school_name'] in ["CSUEastBay", "CSUFullerton", "Loyola", "Maryland", "MSU", "OhioState", "Oklahoma", "UNL"]): 
                            (dataframe['dataframe']).rename(columns = {"PIPS - I constructively criticize other studentâ€™s ideas during class" : column_name}, inplace = True)
                        elif (dataframe['school_name'] in ["KSU", "UTRGV"]): 
                            (dataframe['dataframe']).rename(columns = {"PIPS - I constructively criticize other student’s ideas during class" : column_name}, inplace = True)
                        else: 
                            print("***couldn't find a option for the " + column_name + " question***")
                    ###########################################
                    elif (column_name == "PIPS_Helpful - I constructively criticize other students ideas during class"): 
                        if (dataframe['school_name'] in ["CSUEastBay", "CSUFullerton", "Loyola", "Maryland", "MSU", "OhioState", "Oklahoma"]): 
                            (dataframe['dataframe']).rename(columns = {"PIPS_Helpful - I constructively criticize other studentâ€™s ideas during class" : column_name}, inplace = True)
                        elif (dataframe['school_name'] in ["KSU", "UTRGV"]): 
                            (dataframe['dataframe']).rename(columns = {"PIPS_Helpful - I constructively criticize other student’s ideas during class" : column_name}, inplace = True)
                        elif (dataframe['school_name'] in ["UNL"]): 
                            (dataframe['dataframe']).rename(columns = {"PIPS_Helpful - I constructively criticize other student's ideas during class" : column_name}, inplace = True)
                        else: 
                            print("***couldn't find a option for the " + column_name + " question***")
                    ###########################################
                    elif (column_name == "PIPS_Lab - I constructively criticize other students ideas during class"): 
                        if (dataframe['school_name'] in ["CSUEastBay", "CSUFullerton", "Loyola", "Maryland", "MSU", "OhioState", "Oklahoma", "UNL"]): 
                            (dataframe['dataframe']).rename(columns = {"PIPS_Lab - I constructively criticize other studentâ€™s ideas during class" : column_name}, inplace = True)
                        elif (dataframe['school_name'] in ["UTRGV"]): 
                            (dataframe['dataframe']).rename(columns = {"PIPS_Lab - I constructively criticize other student’s ideas during class" : column_name}, inplace = True)
                        elif (dataframe['school_name'] == "KSU"): 
                            (dataframe['dataframe']).insert(index, column_name, "")
                        else:
                            print("***couldn't find a option for the " + column_name + " question***")
                    ###########################################
                    elif (column_name == "Please indicate your level of agreement for the following statements from the beginning of the co... - Beginning of course - I can learn from hearing other peoples mathematical thinking, even if their thinking is not correct."): 
                        if (dataframe['school_name'] in ["CSUEastBay", "CSUFullerton", "Loyola", "Maryland", "MSU", "OhioState", "Oklahoma"]): 
                            (dataframe['dataframe']).rename(columns = {"Please indicate your level of agreement for the following statements from the beginning of the co... - Beginning of course - I can learn from hearing other peopleâ€™s mathematical thinking, even if their thinking is not correct." : column_name}, inplace = True)
                        elif (dataframe['school_name'] in ["KSU", "UTRGV"]): 
                            (dataframe['dataframe']).rename(columns = {"Please indicate your level of agreement for the following statements from the beginning of the co... - Beginning of course - I can learn from hearing other people’s mathematical thinking, even if their thinking is not correct." : column_name}, inplace = True)
                        elif (dataframe['school_name'] in ["UNL"]): 
                            (dataframe['dataframe']).rename(columns = {"Please indicate your level of agreement for the following statements from the beginning of the co... - Beginning of course - I can learn from hearing other people's mathematical thinking, even if their thinking is not correct." : column_name}, inplace = True)
                        else: 
                            print("***couldn't find a option for the " + column_name + " question***")
                    ###########################################
                    elif (column_name == "Please indicate your level of agreement for the following statements from the beginning of the co... - Now - I can learn from hearing other peoples mathematical thinking, even if their thinking is not correct."): 
                        if (dataframe['school_name'] in ["CSUEastBay", "CSUFullerton", "Loyola", "Maryland", "MSU", "OhioState", "Oklahoma"]): 
                            (dataframe['dataframe']).rename(columns = {"Please indicate your level of agreement for the following statements from the beginning of the co... - Now - I can learn from hearing other peopleâ€™s mathematical thinking, even if their thinking is not correct." : column_name}, inplace = True)
                        elif (dataframe['school_name'] in ["KSU", "UTRGV"]): 
                            (dataframe['dataframe']).rename(columns = {"Please indicate your level of agreement for the following statements from the beginning of the co... - Now - I can learn from hearing other people’s mathematical thinking, even if their thinking is not correct." : column_name}, inplace = True)
                        elif (dataframe['school_name'] in ["UNL"]): 
                            (dataframe['dataframe']).rename(columns = {"Please indicate your level of agreement for the following statements from the beginning of the co... - Now - I can learn from hearing other people's mathematical thinking, even if their thinking is not correct." : column_name}, inplace = True)
                        else: 
                            print("***couldn't find a option for the " + column_name + " question***")
                    ###########################################
                    elif (column_name == "SpecialPop - First-generation college student (i.e., neither parent nor guardian completed a Bachelors degree)"): 
                        if (dataframe['school_name'] in ["CSUEastBay", "CSUFullerton", "Loyola", "Maryland", "OhioState", "Oklahoma"]): 
                            (dataframe['dataframe']).rename(columns = {"SpecialPop - First-generation college student (i.e., neither parent nor guardian completed a Bachelorâ€™s degree)" : column_name}, inplace = True)
                        elif (dataframe['school_name'] in ["UNL"]): 
                            (dataframe['dataframe']).rename(columns = {"SpecialPop - First-generation college student (i.e., neither parent nor guardian completed a Bachelor's degree)" : column_name}, inplace = True)
                        elif dataframe['school_name'] in ["KSU", "MSU", "UTRGV"]: 
                            (dataframe['dataframe']).insert(index, column_name, "")
                        else: 
                            print("***couldn't find a option for the " + column_name + " question***")
                    ###########################################
                    else: 
                        (dataframe['dataframe']).insert(0, column_name, "")
            (dataframe['dataframe']).insert(0, "School", dataframe['school_name'])
        frames = []
        column_names.insert(0, "School")
        for dataframe in dataframe_hold: 
            frames.append((dataframe['dataframe'])[column_names])
        (pandas.concat(frames)).to_csv("combine.csv", index = False)




path_to_clean = r"C:\Users\mting\Desktop\Work\Seminal\data\spips\spring2019\clean" 
path_to_columnNames = r"C:\Users\mting\Desktop\Work\Seminal\seminalcode\SPIPS\Spring2019\columnnames-SPIPsp2019.txt"

putting_it_together = putTogether(path_to_clean, path_to_columnNames)
putting_it_together.readinFiles()