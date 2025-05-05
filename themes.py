### cs32_fp/themes.py
import random

class ThemeManager:
    def __init__(self, theme_names, base_path="themed_q_a"):
        self.themes = theme_names # list of theme names
        self.base_path = base_path # folder where themed text files are stored 
        self.qa_dict = {}  # maps to dictionary of questions and answers
        self.asked_questions = {theme: set() for theme in theme_names} #tracks what questions have been asked
        self.load_all_themes() #loading the text files into the themes

    # loads all question-answer pairs from text files into qa_dict
    def load_all_themes(self):
        for theme in self.themes:
            # builds the file path based on theme name, replacing spaces with hyphens
            file_path = f"{self.base_path}/{theme.replace(" ", "-")}-qa.txt"
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    qas = {}
                    # reads two lines at a time, question then answer 
                    for i in range(0, len(lines), 2):
                        question = lines[i].strip()[3:] # remove 'Q: ' from the line
                        answer = lines[i+1].strip()[3:] # remove 'A: ' from the line
                        qas[question] = answer # stores the pair in the themes directory 
                    self.qa_dict[theme] = qas
            except FileNotFoundError:
                # if the file doesn't exist, warn user and use an empty theme
                print(f"File not found for theme '{theme}'. Skipping.")
                self.qa_dict[theme] = {}

    # returns a list of themes that still have unused questions
    def get_available_themes(self):
        available = []
        for theme in self.themes:
            # checks if there are still questions left in this theme
            if len(self.asked_questions[theme]) < len(self.qa_dict[theme]):
                available.append(theme)
        return available

    def has_questions(self, theme):
        return len(self.asked_questions[theme]) < len(self.qa_dict[theme])

    # selects and returns unused question from the given theme
    def get_random_question(self, theme):
        # if no questions left, raise an error
        if not self.has_questions(theme):
            raise ValueError(f"No more questions left in theme '{theme}'.")

        all_qs = list(self.qa_dict[theme].keys())
        unused_qs = [q for q in all_qs if q not in self.asked_questions[theme]] # filter out already used questions
        q = random.choice(unused_qs) # pick one at random
        self.asked_questions[theme].add(q) # mark it as asked 
        return q, self.qa_dict[theme][q] # return the question and its corresponding answer
