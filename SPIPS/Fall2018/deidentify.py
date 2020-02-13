import pandas

class RemoveName: 
    def __init__(self, path_to_file, path_to_stopwords):
        self.path_to_file = path_to_file
        self.path_to_stopwords = path_to_stopwords

    def BeginRemoval(self):
        df = pandas.read_csv(self.path_to_file)
        text_columns = ["OpenHelpful"]
        # "OpenUnhelpful", "TechUse - Other (please specify): - Text", 
        # "TutoringSource - Tutoring center at [Field-Site] (please identify the center): - Text", "TutoringSource - Other (please explain) - Text", 
        # "IdentityFR", "AnythingElse", "Preparation - No (please explain) - Text"]
        with open(self.path_to_stopwords) as fp: 
            stopwords = [stopword[:-1] for stopword in fp]
        for column in text_columns: 
            for row in range(0, df.shape[0]): 
                free_response = df[column][row].lower()
                if any(word in free_response for word in stopwords): 
                    print(free_response)
                    print("***stopword found, please edit***")
                    new_response = input()
                    print("Is this correct?")
                    print("Press 'e' to edit. Press any key to continue")
                    correct = input()
                    while correct == 'e': 
                        print("***please edit***")
                        new_response = input()
                        print("Is this correct?")
                        print("Press 'e' to edit. Press any key to continue")
                        correct = input()
                    df.iat[row, df.columns.get_loc(column)] = new_response
        df.to_csv("test.csv", index = False)

test = RemoveName(r"C:\Users\mting\Desktop\Work\Seminal\data\spips\fall2018\combine\test.csv", r"C:\Users\mting\Desktop\Work\Seminal\seminalcode\SPIPS\Fall2018\stopwords.txt")
test.BeginRemoval() 