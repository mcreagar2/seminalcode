import pandas

class RemoveName: 
    def __init__(self, path_to_file, path_to_stopwords):
        self.path_to_file = path_to_file
        self.path_to_stopwords = path_to_stopwords

    def BeginRemoval(self):
        df = pandas.read_csv(self.path_to_file)
        one_percent = df.shape[0]/100
        current_percent = one_percent
        percent_count = 1
        text_columns = ["OpenHelpful", "OpenUnhelpful", "TechUse - Other (please specify): - Text", 
        "TutoringSource - Tutoring center at [Field-Site] (please identify the center): - Text", "TutoringSource - Other (please explain) - Text", 
        "IdentityFR", "AnythingElse", "Preparation - No (please explain) - Text"]
        with open(self.path_to_stopwords) as fp: 
            stopwords = [stopword[:-1].lower() for stopword in fp]
        for column in text_columns: 
            print("Checking " + column)
            for row in range(0, df.shape[0]): 
                free_response = str(df[column][row])
                hit = False
                if free_response != 'nan': 
                    for response_word in free_response.split(): 
                        if response_word.lower() in stopwords: 
                            hit = True
                            print("Stop word *" + response_word + "* found in:")
                            print("***" + free_response + "***")
                            print("press 'enter' to pass or type anything to edit")
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
                        if hit: 
                            break
                if row > current_percent: 
                    print(str(percent_count)+"%")
                    current_percent = current_percent + one_percent
                    percent_count = percent_count + 1
            print("Press 's' to save and quit or any key to continue")
            saving = input()
            if saving == 's': 
                df.to_csv("test.csv", index = False)
                break
        df.to_csv("test.csv", index = False)

test = RemoveName(r"C:\Users\mting\Desktop\Work\Seminal\data\spips\fall2018\combine\SPIPsFall2018Combine.csv", r"C:\Users\mting\Desktop\Work\Seminal\seminalcode\SPIPS\Fall2018\stopwords.txt")
test.BeginRemoval() 