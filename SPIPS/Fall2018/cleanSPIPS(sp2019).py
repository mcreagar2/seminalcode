import os 
import numpy as np 
import pandas 
from pandas import DataFrame

class Cleaner:
    def __init__(self, numeric_path, text_path, clean_path): 
        self.numeric_path = numeric_path
        self.text_path = text_path
        self.clean_path = clean_path
        self.clean_year = ""
        self.clean_semester = ""

    def findBothFiles(self): 
        numeric_hold = os.listdir(self.numeric_path)
        text_hold = os.listdir(self.text_path)
        numeric_hold.sort()
        text_hold.sort()
        try:
            for index in range(0, len(numeric_hold)): 
                if((numeric_hold[index].split("_")[0]) != (text_hold[index].split("_")[0])): 
                    print("***One of these files does not have a pair***")
                    print(numeric_hold[index])
                    print(text_hold[index])
                    break
        except IndexError: 
            print("***You have uneven number of files or one of the files is open***")
            return
        print("Looks good! Reading {} files, lets start".format(len(numeric_hold)))
        print("Make sure all files have a '.xlsx' extenstion")
        print("Year that is being cleaned")
        self.clean_year = input()
        print("Semester being cleaned")
        self.clean_semester = input()

        for index in range(0, len(numeric_hold)): 
            numeric_file = os.path.join(self.numeric_path, numeric_hold[index])
            text_file = os.path.join(self.text_path, text_hold[index])
            print("Cleaning " + numeric_hold[index] + " and " + text_hold[index])
            self.cleanFiles(numeric_file, text_file)
            if index < len(numeric_hold)-1:
                print("Done, next file?")
                cont = input()
            else: 
                print("Done")

    def cleanFiles(self, numeric_file, text_file): 
        numeric_df = pandas.read_excel(numeric_file)
        text_df = pandas.read_excel(text_file)
        merged_dataframe = (numeric_df)
        
        file_name_hold = numeric_file.split("\\")[len(numeric_file.split("\\"))-1]
        file_name_hold = file_name_hold.split("_")
        school_name = file_name_hold[0]
        school_year = file_name_hold[len(file_name_hold)-1].split(".")[0]

        
        text_bank = ["Enrolled course - Course", "Enrolled course - Lecture Section", "Enrolled course - Schedule", 
        "Enrolled course - Instructor", "Which recitation section are you currently enrolled in for [QID7-ChoiceGroup-SelectedAnswers-1]? - Course", 
        "Which recitation section are you currently enrolled in for [QID7-ChoiceGroup-SelectedAnswers-1]? - Recitation Section", 
        "Which recitation section are you currently enrolled in for [QID7-ChoiceGroup-SelectedAnswers-1]? - Schedule", 
        "Which recitation section are you currently enrolled in for [QID7-ChoiceGroup-SelectedAnswers-1]? - Instructor", "Next class - Selected Choice",
        "Next class - Other: - Text"]

        print("Copying text columns...")
        for index in range(0, len(text_bank)): 
            try:
                merged_dataframe[[text_bank[index]]] = text_df[[text_bank[index]]]
            except KeyError: 
                print("***Column '{}' not found***".format(text_bank[index]))
        print("done")

        print("Deleting distribution channel...")
        # delete distribution channel 
        try:
            merged_dataframe = merged_dataframe.drop(columns=['Distribution Channel'])
            print("done")
        except KeyError: 
            print("***No Distribution Channel Found***")

        print("Deleting nonconsenting rows")
        # drop rows that do not consent 
        try: 
            droplist = []
            for index in range(0, merged_dataframe.shape[0]): 
                if (((merged_dataframe.iloc[index]["ConsentAll"] == 2) and (merged_dataframe.iloc[index]["ConsentPart"] == 2)) or (merged_dataframe.iloc[index]["Over18"] == 2)) or ((merged_dataframe.iloc[index]["ConsentAll"] == 2) and (pandas.isnull(merged_dataframe.iloc[index]["ConsentPart"]) is True)): 
                    droplist.append(index)
            merged_dataframe.drop(merged_dataframe.index[droplist], inplace = True)
            merged_dataframe.index = pandas.RangeIndex(len(merged_dataframe.index))
            print("done --{} removed--".format(len(droplist)))
        except KeyError:
            try: 
                droplist = []
                for index in range(0, merged_dataframe.shape[0]): 
                    if ((merged_dataframe.iloc[index]["You are\nvoluntarily making a decision whether or not to participate in this research study.  Your agreement to participate is indicated by checking\none of the boxes below and typing your name. You should print a\ncopy of this agreement for your records."] == 2)): 
                        droplist.append(index)
                merged_dataframe.drop(merged_dataframe.index[droplist], inplace = True)
                merged_dataframe.index = pandas.RangeIndex(len(merged_dataframe.index))
                print("done --{} removed--".format(len(droplist)))
            except KeyError: 
                try: 
                    droplist = []
                    for index in range(0, merged_dataframe.shape[0]): 
                        if ((merged_dataframe.iloc[index]["ConsentAll"] == 2) and (merged_dataframe.iloc[index]["ConsentPart"] == 2)): 
                            droplist.append(index)
                    merged_dataframe.drop(merged_dataframe.index[droplist], inplace = True)
                    merged_dataframe.index = pandas.RangeIndex(len(merged_dataframe.index))
                    print("done --{} removed--".format(len(droplist)))
                except KeyError: 
                    try: 
                        droplist = []
                        for index in range(0, merged_dataframe.shape[0]): 
                            if ((merged_dataframe.iloc[index]["Consent - Survey"] == 2) or (merged_dataframe.iloc[index]["Age eligibility"] == 2)): 
                                droplist.append(index)
                        merged_dataframe.drop(merged_dataframe.index[droplist], inplace = True)
                        merged_dataframe.index = pandas.RangeIndex(len(merged_dataframe.index))
                        print("done --{} removed--".format(len(droplist)))
                    except KeyError: 
                        try: 
                            droplist = []
                            for index in range(0, merged_dataframe.shape[0]): 
                                if ((merged_dataframe.iloc[index]["ConsentAll"] == 2)): 
                                    droplist.append(index)
                            merged_dataframe.drop(merged_dataframe.index[droplist], inplace = True)
                            merged_dataframe.index = pandas.RangeIndex(len(merged_dataframe.index))
                            print("done --{} removed--".format(len(droplist)))
                        except KeyError: 
                            print("***Something is up with the Consent Column. Please fix this and come back to me***")
                            return
            
        print("Checking age column")
        print("You can edit by entering an integer, delete(d) the row, leave(l) the cell the way it is, or make it blank(b)")
        # delete under 18 year-olds, allows controller to edit/ some age responses that are not correct 
        droplist = []
        for index in range(0, merged_dataframe.shape[0]): 
            # if age is less than 18, drop from list 
            correct_response = True
            try: 
                if  merged_dataframe.iloc[index]['Age'] > 110: 
                    correct_response = False
                    print("'{}'was an incorrect entry".format(merged_dataframe.iloc[index]['Age']))
                elif merged_dataframe.iloc[index]['Age'] < 18: 
                    droplist.append(index)
            # if there is a type error, edit, delete, or leave blank 
            except TypeError: 
                correct_response = False
                print("'{}' was an incorrect entry".format(merged_dataframe.iloc[index]['Age']))
            while(correct_response is False): 
                command_list = ['d', 'l', 'b']
                user_command = input()
                try: 
                    if user_command in command_list:
                        # once correct response is given, check input 
                        if user_command == 'd':
                            droplist.append(index)
                            correct_response = True
                        elif user_command == 'b': 
                            merged_dataframe.iat[index, merged_dataframe.columns.get_loc('Age')] = np.nan
                            correct_response = True
                        else: 
                            correct_response = True
                    elif int(user_command) > 17 and int(user_command) < 110:
                            merged_dataframe.iat[index, merged_dataframe.columns.get_loc('Age')] = int(user_command)
                            correct_response = True
                    else: 
                        print("You can edit by entering an integer, delete(d) the row, leave(l) the cell the way it is, or make it blank(b)")
                except ValueError: 
                    print("You can edit by entering an integer, delete(d) the row, leave(l) the cell the way it is, or make it blank(b)")
        merged_dataframe.drop(merged_dataframe.index[droplist], inplace = True)
        merged_dataframe.index = pandas.RangeIndex(len(merged_dataframe.index))
        print("done --{} removed--".format(len(droplist)))

        print("Finding duplicates...")
        # find duplicates 
        try: 
            if isthisOhioState: 
                student_id_text = "Student ID"
            else: 
                student_id_text = "StudentID"
            found_ids = []
            droplist = []
            error1_hold = []
            error2_hold = []
            for index in range(0, merged_dataframe.shape[0]): 
                duplicate_hold = merged_dataframe.loc[merged_dataframe[student_id_text] == merged_dataframe.iloc[index][student_id_text]]
                # if duplicates found, find most complete 
                if (duplicate_hold.shape[0] > 1) and (merged_dataframe.iloc[index][student_id_text] not in found_ids): 
                    duplicate_id = merged_dataframe.iloc[index][student_id_text]
                    found_ids.append(duplicate_id)
                    best_row = 0 
                    highest_completeness = 0 
                    # find most complete row, judging by most number of complete cells 
                    for row in range(0, duplicate_hold.shape[0]): 
                        current_completeness = 0 
                        for column in range(0, duplicate_hold.shape[1]): 
                            if pandas.isnull(duplicate_hold.iloc[row][column]) is False: 
                                current_completeness += 1
                        if current_completeness > highest_completeness: 
                            best_row = row
                            highest_completeness = current_completeness
                    # get row index from a dataframe copy 
                    duplicate_rows_index = merged_dataframe.index[merged_dataframe[student_id_text] == duplicate_id].tolist()
                    # known columns that contain short response text 
                    text_columns =["OpenHelpful", "OpenUnhelpful", "TechUse - Other (please specify): - Text", "TutoringSource - Other (please explain) - Text", 
                    "TutoringSource - Tutoring center at [Field-Site] (please identify the center): - Text", "TutoringSource - Tutoring center at Morgan State University  (please identify the center): - Text", 
                    "What specific teaching strategies does your instructor use to promote equitable and inclusive stu...", "What specific teaching strategies does your instructor use to promote equitable and inclusive student engagement?", 
                    "How (if at all) has your experience in this course differed from last term?", "Gender - Not listed (please specify): - Text", "EthnoRacial - Not listed (please specify): - Text", 
                    "SexualOrientation - Not listed (please specify): - Text", "ClassRank - Other (please specify) - Text", "Major_Text", "Preparation - No (please explain) - Text", "NextCourse - TEXT", 
                    "NextCourse - Other - Text", "NextCourse - Other (please explain) - Text", "IdentityFR", "AnythingElse", "Contact - Yes, here is my contact email: - Text"]
                    index = 0 
                    end_index = len(text_columns)
                    # try to take text from duplicate rows and add to most complete row 
                    while index < end_index: 
                        duplicate_text = ""
                        try: 
                            for row in range(0, duplicate_hold.shape[0]): 
                                if row is not best_row and pandas.isnull(merged_dataframe.iloc[duplicate_rows_index[row]][text_columns[index]]) is False:     
                                    duplicate_text = duplicate_text + " [[Dupe Comment: " + str(merged_dataframe.iloc[duplicate_rows_index[row]][text_columns[index]]) + "]]"
                            if pandas.isnull(merged_dataframe.iloc[duplicate_rows_index[best_row]][text_columns[index]]): 
                                merged_dataframe.iat[duplicate_rows_index[best_row], merged_dataframe.columns.get_loc(text_columns[index])] = duplicate_text
                            else: 
                                merged_dataframe.iat[duplicate_rows_index[best_row], merged_dataframe.columns.get_loc(text_columns[index])] = str(merged_dataframe.iloc[duplicate_rows_index[best_row]][text_columns[index]]) + duplicate_text
                        except KeyError: 
                            if index not in error1_hold: 
                                error1_hold.append(index)
                        except ValueError:
                            if index not in error2_hold:  
                                error2_hold.append(index)
                        index += 1 
                    for row in range(0, len(duplicate_rows_index)): 
                        if row is not best_row: 
                            droplist.append(duplicate_rows_index[row])                  
            # drop duplicate rows       
            for error_index in error1_hold: 
                print("***" + text_columns[error_index] + " does not exist***")
            for error_index in error2_hold: 
                print("***" + text_columns[error_index] + " has a problem. It might be blank (which isn't a problem). ValueError thrown***")
            merged_dataframe.drop(merged_dataframe.index[droplist], inplace = True)
            merged_dataframe.index = pandas.RangeIndex(len(merged_dataframe.index))
            print("done --{} removed--".format(len(droplist)))
        except KeyError: 
            print("***I couldn't find a StudentID column. Continue?***")
            input()



        # print("Generating row stats...")
        # #create metric of student survey completeness 
        # question_eleven = [merged_dataframe.columns.get_loc("PIPS - I listen as the instructor guides me through major topics"), merged_dataframe.columns.get_loc("PIPS_Helpful - My instructor uses strategies to encourage participation from a wide range of students")]
        # question_twelve = [merged_dataframe.columns.get_loc("PIPS_Lab - I listen as the instructor guides me through major topics"), merged_dataframe.columns.get_loc("PIPS_Lab - My instructor uses strategies to encourage participation from a wide range of students")]
        # question_sixteen = [merged_dataframe.columns.get_loc("Included_Class - How much opportunity do you get to answer questions in class?"), merged_dataframe.columns.get_loc("Included_Class - How much praise does your work receive?")]
        # question_seventeen = [merged_dataframe.columns.get_loc("Included_Lab - How much opportunity do you get to answer questions in class?"), merged_dataframe.columns.get_loc("Included_Lab - How much praise does your work receive?")]
        # question_eightteen = [merged_dataframe.columns.get_loc("Climate - Excluding and Hostile:Including and Friendly"), merged_dataframe.columns.get_loc("Climate - Academically easy:Academically rigorous")]
        # question_twenty = [merged_dataframe.columns.get_loc("Attitude - Beginning of course - I am interested in mathematics"), merged_dataframe.columns.get_loc("Attitude - Now - I feel anxious when working with others on mathematics during class")]
        # question_other = [merged_dataframe.columns.get_loc("Please indicate your level of agreement for the following statements from the beginning of the co... - Beginning of course - I can learn from hearing other peopleâ€™s mathematical thinking, even if their thinking is not correct."), merged_dataframe.columns.get_loc("Please indicate your level of agreement for the following statements from the beginning of the co... - Now - I enjoy figuring out math problems with other people.")]
        # demo_gender = [merged_dataframe.columns.get_loc("Gender - Selected Choice - Man"), merged_dataframe.columns.get_loc("Gender - Not listed (please specify): - Text")]
        # demo_ethno = [merged_dataframe.columns.get_loc("EthnoRacial - Selected Choice - Alaskan Native or Native American"), merged_dataframe.columns.get_loc("EthnoRacial - Not listed (please specify): - Text")]
        # demo_orientation = [merged_dataframe.columns.get_loc("SexualOrientation - Selected Choice - Asexual"), merged_dataframe.columns.get_loc("SexualOrientation - Not listed (please specify): - Text")]
        # #demo_four = [merged_dataframe.columns.get_loc("SpecialPop - International student"), merged_dataframe.columns.get_loc("SpecialPop - Prefer not to disclose")]
        
        # question_hold = [question_eleven, question_twelve, question_sixteen, question_seventeen, question_eightteen, question_twenty, question_other]
        # demo_hold = [demo_gender, demo_ethno, demo_orientation]

        # stat_col_names = ['q-11', 'q-12', 'q-16', 'q-17', 'q-18', 'q-20', 'q-other', 'd-gender', 'd-ethno', 'd-orientation']
        # stat_list = []

        # if (len(question_hold) + len(demo_hold)) != len(stat_col_names): 
        #     print("You have an unequal number of stat headers to your stat questions")
        #     return  

        # for row in range(0, merged_dataframe.shape[0]): 
        #     stat_hold = []
        #     for question in question_hold: 
        #         blank_count = 0 
        #         for index in range(question[0], question[1]+1): 
        #             if pandas.isnull(merged_dataframe.iloc[row][index]): 
        #                 blank_count += 1
        #         stat_hold.append(round(1-(blank_count/(question[1]+1-question[0])), 2))
        #     for demographic in demo_hold: 
        #         answered = False
        #         for index in range(demographic[0], demographic[1]+1): 
        #             if pandas.isnull(merged_dataframe.iloc[row][index]) is False: 
        #                 answered = True
        #         if answered: 
        #             stat_hold.append(1)
        #         else: 
        #             stat_hold.append(0)
        #     stat_list.append(stat_hold)
        # stats_dataframe = DataFrame(data = stat_list, columns = stat_col_names)
        # print("done")



        print("Putting it all together...")
        # put it all together 
        #frames = [merged_dataframe, stats_dataframe]
        #merged_dataframe = pandas.concat(frames, axis = 1, join = 'inner')
        file_name = self.clean_path + school_name + "_Clean_SPIPS_" + self.clean_semester + self.clean_year + ".xlsx"
        merged_dataframe.to_excel(file_name, index = False)


numeric_path = r"C:\Users\mting\Desktop\Work\seminal\data\spips\spring2019\numeric"
text_path = r"C:\Users\mting\Desktop\Work\seminal\data\spips\spring2019\text"
clean_path = r"C:\\Users\\mting\\Desktop\\Work\\seminal\\data\\spips\\spring2019\\clean\\"
cleantest = Cleaner(numeric_path, text_path, clean_path) 
cleantest.findBothFiles()