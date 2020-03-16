import pandas
import re

class RemoveName: 
    def __init__(self, path_to_file, path_to_stopwords):
        self.path_to_file = path_to_file
        self.path_to_stopwords = path_to_stopwords

    def BeginRemoval(self):
        df = pandas.read_excel(self.path_to_file)
        if df.shape[0] < 100: 
            ten_percent = df.shape[0]/10
            small = True
            percent_count = 10
            current_percent = ten_percent
        else: 
            one_percent = df.shape[0]/100
            small = False
            percent_count = 1
            current_percent = one_percent
        text_columns = ["OpenHelpful", "OpenUnhelpful", "TechUse - Other (please specify): - Text", "TutoringSource - Tutoring center at [Field-Site] (please identify the center): - Text", "TutoringSource - Other (please explain) - Text", "What specific teaching strategies does your instructor use to promote equitable and inclusive student engagement?", "How (if at all) has your experience in this course differed from last term?", "NextCourse - Other (please explain) - Text", "IdentityFR", "AnythingElse"]
        with open(self.path_to_stopwords) as fp: 
            stopwords = [stopword[:-1].lower() for stopword in fp]
        for column in text_columns: 
            print("Checking " + column)
            if small is False:
                current_percent = one_percent
                percent_count = 1
            elif small is True:
                current_percent = ten_percent
                percent_count = 10 
            for row in range(0, df.shape[0]): 
                free_response = str(df[column][row])
                hit = False
                if free_response != 'nan': 
                    for response_word in re.split("[ . , ' ! @ # $ % ^ & * ( ) _ - + = : ; \ | ~ ` < > / ?]", free_response): 
                        if response_word.lower() in stopwords and hit is False: 
                            hit = True
                            print("Stop word *" + response_word + "* found in:")
                            print("***" + free_response + "***")
                            print("press 'enter' to pass, 'r' to remove the stop word from the stop list, or type anything to edit")
                            new_response = input()
                            if new_response != "" and new_response != 'r':
                                print("Is this correct?")
                                print("Press 'e' to edit. Press any key to continue")
                                correct = input()
                                while correct == 'e': 
                                    print("---please edit---")
                                    new_response = input()
                                    print("Is this correct?")
                                    print("Press 'e' to edit. Press any key to continue")
                                    correct = input()
                                df.iat[row, df.columns.get_loc(column)] = new_response
                            elif new_response == 'r': 
                                stopwords = [good_stopword for good_stopword in stopwords if good_stopword != response_word.lower()]
                                print("Stop word *" + response_word +"* removed from list")
                                print("Enter to pass current entry, type anything to edit")
                                new_response = input()
                                if new_response != "":
                                    print("Is this correct?")
                                    print("Press 'e' to edit. Press any key to continue")
                                    correct = input()
                                    while correct == 'e': 
                                        print("---please edit---")
                                        new_response = input()
                                        print("Is this correct?")
                                        print("Press 'e' to edit. Press any key to continue")
                                        correct = input()
                                    df.iat[row, df.columns.get_loc(column)] = new_response
                            else:
                                pass
                        if hit: 
                            break
                if row > current_percent and small is False: 
                    print(str(percent_count)+"%")
                    current_percent = current_percent + one_percent
                    percent_count = percent_count + 1
                elif row > current_percent and small is True: 
                    print(str(percent_count)+"%")
                    current_percent = current_percent + ten_percent
                    percent_count = percent_count + 10
            print("Press 's' to save and quit or any key to continue")
            saving = input()
            if saving == 's': 
                df.to_csv("test.csv", index = False)
                with open('newstopwords.txt', 'w') as filehandle:
                    for listitem in stopwords:
                        filehandle.write('%s\n' % listitem)
                break
        df.to_csv("test.csv", index = False)
        with open('newstopwords.txt', 'w') as filehandle:
            for listitem in stopwords:
                filehandle.write('%s\n' % listitem)

test = RemoveName(r"C:\Users\mting\Desktop\Work\Seminal\data\spips\fall2019\text\CSUF_Text_SPIPS_Fall2019.xlsx", r"C:\Users\mting\Desktop\Work\Seminal\seminalcode\SPIPS\Fall2019\stopwords.txt")
test.BeginRemoval() 