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
        bad_column_names = ["PIPS - I constructively criticize other studentâ€™s ideas during class", 
        "PIPS_Helpful - I constructively criticize other studentâ€™s ideas during class", 
        "PIPS_Lab - I constructively criticize other studentâ€™s ideas during class", 
        "Please indicate your level of agreement for the following statements from the beginning of the co... - Beginning of course - I can learn from hearing other peopleâ€™s mathematical thinking, even if their thinking is not correct.", 
        "Please indicate your level of agreement for the following statements from the beginning of the co... - Now - I can learn from hearing other peopleâ€™s mathematical thinking, even if their thinking is not correct.", 
        "SpecialPop - First-generation college student (i.e., neither parent nor guardian completed a Bachelorâ€™s degree)"]
        for dataframe in dataframe_hold: 
            bad_index = 0
            for index, column_name in enumerate(column_names): 
                if column_name not in (dataframe['dataframe']).columns.tolist(): 
                    # all exceptions found by hand 
                    ###########################################
                    if dataframe['school_name'] == "MSU" and column_name == "OverallExp - I attend tutoring sessions or seek help outside of class time": 
                        (dataframe['dataframe']).rename(columns = {"OverallExp - I attend tutoring sessions outside of class time" : column_name}, inplace = True)
                    ###########################################
                    elif dataframe['school_name'] == "MSU" and column_name == "EnrolledCourse - Recitation/Lab Section": 
                        (dataframe['dataframe']).rename(columns = {"EnrolledCourse - Discussion/Lab Section" : column_name}, inplace = True)
                    ###########################################
                    elif dataframe['school_name'] == "KSU" and column_name == "TechUse - Selected Choice - Learning management systems (e.g., Blackboard, Canvas, Piazza)": 
                        (dataframe['dataframe']).rename(columns = {"TechUse - Selected Choice - Learning management systems (e.g., D2L, Blackboard, Canvas, Piazza)" : column_name}, inplace = True)
                    ###########################################
                    elif dataframe['school_name'] == "Maryland" and column_name == "Climate - Excluding and Hostile:Including and Friendly": 
                        (dataframe['dataframe']).rename(columns = {"Climate - Including and Friendly" : column_name}, inplace = True)
                    ###########################################
                    elif dataframe['school_name'] == "Maryland" and column_name == "Climate - Intellectually boring:Intellectually engaging": 
                        (dataframe['dataframe']).rename(columns = {"Climate - Intellectually engaging" : column_name}, inplace = True)
                    ###########################################
                    elif dataframe['school_name'] == "Maryland" and column_name == "Climate - Academically easy:Academically rigorous": 
                        (dataframe['dataframe']).rename(columns = {"Climate - Academically Rigorous" : column_name}, inplace = True)
                    ###########################################
                    elif dataframe['school_name'] == "Maryland" and column_name == "NextCourse - Other (please explain) - Text": 
                        (dataframe['dataframe']).rename(columns = {"NextCourse - Other (please explain): - Text" : column_name}, inplace = True)
                    ###########################################
                    elif column_name == "PIPS - I constructively criticize other students ideas during class" and bad_column_names[bad_index] in (dataframe['dataframe']).columns.tolist(): 
                        bad_index += 1
                        if dataframe['school_name'] == "Maryland": 
                            (dataframe['dataframe']).rename(columns = {"PIPS - I constructively criticize other student‚Äôs ideas during class" : column_name}, inplace = True)
                        else: 
                            (dataframe['dataframe']).rename(columns = {"PIPS - I constructively criticize other studentâ€™s ideas during class" : column_name}, inplace = True)
                    ###########################################
                    elif column_name == "PIPS_Helpful - I constructively criticize other students ideas during class" and bad_column_names[bad_index] in (dataframe['dataframe']).columns.tolist(): 
                        bad_index += 1
                        if dataframe['school_name'] == "Maryland": 
                            (dataframe['dataframe']).rename(columns = {"PIPS_Helpful - I constructively criticize other student‚Äôs ideas during class" : column_name}, inplace = True)
                        else: 
                            (dataframe['dataframe']).rename(columns = {"PIPS_Helpful - I constructively criticize other studentâ€™s ideas during class" : column_name}, inplace = True)
                    ###########################################
                    elif column_name == "PIPS_Lab - I constructively criticize other students ideas during class" and bad_column_names[bad_index] in (dataframe['dataframe']).columns.tolist(): 
                        bad_index += 1
                        if dataframe['school_name'] == "Maryland": 
                            (dataframe['dataframe']).rename(columns = {"PIPS_Lab - I constructively criticize other students ideas during class" : column_name}, inplace = True)
                        else: 
                            (dataframe['dataframe']).rename(columns = {"PIPS_Lab - I constructively criticize other studentâ€™s ideas during class" : column_name}, inplace = True)
                    ###########################################
                    elif column_name == "Please indicate your level of agreement for the following statements from the beginning of the co... - Beginning of course - I can learn from hearing other peoples mathematical thinking, even if their thinking is not correct." and bad_column_names[bad_index] in (dataframe['dataframe']).columns.tolist(): 
                        bad_index += 1 
                        if dataframe['school_name'] == "Maryland": 
                            (dataframe['dataframe']).rename(columns = {"Please indicate your level of agreement for the following statements from the beginning of the co... - Beginning of course - I can learn from hearing other people‚Äôs mathematical thinking, even if their thinking is not correct." : 
                            column_name}, inplace = True)
                        else: 
                            (dataframe['dataframe']).rename(columns = {"Please indicate your level of agreement for the following statements from the beginning of the co... - Beginning of course - I can learn from hearing other peopleâ€™s mathematical thinking, even if their thinking is not correct." : 
                            column_name}, inplace = True)
                    ###########################################
                    elif column_name == "Please indicate your level of agreement for the following statements from the beginning of the co... - Now - I can learn from hearing other peoples mathematical thinking, even if their thinking is not correct." and bad_column_names[bad_index] in (dataframe['dataframe']).columns.tolist(): 
                        bad_index += 1
                        if dataframe['school_name'] == "Maryland": 
                            (dataframe['dataframe']).rename(columns = {"Please indicate your level of agreement for the following statements from the beginning of the co... - Now - I can learn from hearing other people‚Äôs mathematical thinking, even if their thinking is not correct." : 
                            column_name}, inplace = True)
                        else: 
                            (dataframe['dataframe']).rename(columns = {"Please indicate your level of agreement for the following statements from the beginning of the co... - Now - I can learn from hearing other peopleâ€™s mathematical thinking, even if their thinking is not correct." : 
                            column_name}, inplace = True)
                    ###########################################
                    elif column_name == "SpecialPop - First-generation college student (i.e., neither parent nor guardian completed a Bachelors degree)" and bad_column_names[bad_index] in (dataframe['dataframe']).columns.tolist(): 
                        bad_index += 1
                        if dataframe['school_name'] == "Maryland": 
                            (dataframe['dataframe']).rename(columns = {"SpecialPop - First-generation college student (i.e., neither parent nor guardian completed a Bachelor‚Äôs degree)" : 
                            column_name}, inplace = True)
                        else: 
                            (dataframe['dataframe']).rename(columns = {"SpecialPop - First-generation college student (i.e., neither parent nor guardian completed a Bachelorâ€™s degree)" : 
                            column_name}, inplace = True)
                    ###########################################
                    else: 
                        (dataframe['dataframe']).insert(index, column_name, "")
            (dataframe['dataframe']).insert(0, "School", dataframe['school_name'])
        frames = []
        column_names.insert(0, "School")
        for dataframe in dataframe_hold: 
            frames.append((dataframe['dataframe'])[column_names])
        (pandas.concat(frames)).to_csv("combine.csv", index = False)




path_to_clean = r"C:\Users\mting\Desktop\Work\Seminal\data\spips\fall2018\clean" 
path_to_columnNames = r"C:\Users\mting\Desktop\Work\Seminal\seminalcode\columnnames.txt"

putting_it_together = putTogether(path_to_clean, path_to_columnNames)
putting_it_together.readinFiles()