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
                    if (dataframe['school_name'] == "OhioState" and column_name == "NextCourse - Other (please explain) - Text"): 
                        (dataframe['dataframe']).rename(columns = {"NextCourse - Other: - Text" : column_name}, inplace = True)
                    elif (dataframe['school_name'] == "OhioState" and column_name == "Including time spent in class, approximately how many hours per week did you expect to spend on this calculus course (in class, studying, reading, doing homework, etc.) this semester?"):
                        (dataframe['dataframe']).rename(columns = {"Including\ntime spent in class, approximately how many hours per week did you expect to\nspend on this calculus course (in class, studying, reading, doing homework,\netc.) this semester?": column_name}, inplace = True)
                    elif (dataframe['school_name'] == "OhioState" and column_name == "Including this course, how many credit hours are you taking this semester?"):
                        (dataframe['dataframe']).rename(columns = {"Including\nthis course, how many credit hours are you taking this semester?": column_name}, inplace = True)
                    elif (dataframe['school_name'] == "OhioState" and column_name == "Are you the primary caregiver for a dependent?"):
                        (dataframe['dataframe']).rename(columns = {"Are\nyou the primary caregiver for a dependent?": column_name}, inplace = True)
                    elif (dataframe['school_name'] == "OhioState" and column_name == "Did you take calculus in high school?"):
                        (dataframe['dataframe']).rename(columns = {"Did\nyou take calculus in high school?": column_name}, inplace = True)
                    elif (dataframe['school_name'] == "OhioState" and column_name == "Which academic year did you take your last calculus course in high school?"):
                        (dataframe['dataframe']).rename(columns = {"Which\nacademic year did you take your last calculus course in high school?": column_name}, inplace = True)
                    else: 
                        (dataframe['dataframe']).insert(0, column_name, "")
            (dataframe['dataframe']).insert(0, "School", dataframe['school_name'])
        frames = []
        column_names.insert(0, "School")
        for dataframe in dataframe_hold: 
            frames.append((dataframe['dataframe'])[column_names])
        (pandas.concat(frames)).to_csv("combine.csv", index = False)




path_to_clean = r"C:\Users\mting\Desktop\Work\Seminal\data\spips\fall2019\clean" 
path_to_columnNames = r"C:\Users\mting\Desktop\Work\Seminal\seminalcode\SPIPS\Fall2019\columnnames-SPIPfa2019.txt"

putting_it_together = putTogether(path_to_clean, path_to_columnNames)
putting_it_together.readinFiles()