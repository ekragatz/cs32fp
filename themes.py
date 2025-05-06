### cs32_fp/themes.py
# This file defines ThemeManager class, which handles loading trivia questions and answers from text files, organzing them by theme, and tracking which questions have already been asked.
# Used by main trivia game to manage themed question sets
import random

# this class manages all the trivia themes and their questions
class ThemeManager:

    def __init__(self, theme_names, base_path="themed_q_a"):
        self.themes = theme_names # list of theme names
        self.base_path = base_path # folder where question and answer text files are stored
        self.qa_dict = {}  # maps to dictionary of questions and answers
        self.asked_questions = {
            theme: set()
            for theme in theme_names
        }  #tracks what questions have been asked
        self.load_all_themes()  #loading the text files into the themes

    # loads questions and answers from each theme file
    def load_all_themes(self):
        for theme in self.themes:
            # replace spaces with underscores and build the full path to the theme's text file
            file_path = f"{self.base_path}/{theme.replace(' ', '_')}_qa.txt"
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    qas = {}
                    # go through the lines two at a time (question then answer)
                    for i in range(0, len(lines), 2): 
                        question = lines[i].strip()[3:] # remove "Q: "
                        answer = lines[i + 1].strip()[3:] # remove "A: "
                        qas[question] = answer # store all questions and answers for this theme
                    self.qa_dict[theme] = qas
            except FileNotFoundError:
                # if the file doesn't exist, skip and use an empty set of questions
                print(f"File not found for theme '{theme}'. Skipping.")
                self.qa_dict[theme] = {}

    # returns a list of themes that still have unused questions
    def get_available_themes(self):
        available = []
        for theme in self.themes:
            # only add themes that have questions left to ask
            if len(self.asked_questions[theme]) < len(self.qa_dict[theme]):
                available.append(theme)
        return available

    # returns true if the theme still has unused questions
    def has_questions(self, theme):
        return len(self.asked_questions[theme]) < len(self.qa_dict[theme])

    def get_random_question(self, theme):
        if not self.has_questions(theme):
            raise ValueError(f"No more questions left in theme '{theme}'.")

        all_qs = list(self.qa_dict[theme].keys())
        unused_qs = [q for q in all_qs if q not in self.asked_questions[theme]]
        q = random.choice(unused_qs)
        self.asked_questions[theme].add(q)
        return q, self.qa_dict[theme][q]

    # picks a random question from a theme that hasn't been asked yet
    def get_random_question(self, theme):
        if not self.has_questions(theme):
            raise ValueError(f"No more questions left in theme '{theme}'.")
        all_qs = list(self.qa_dict[theme].keys()) # get all questions in the theme
        new_qs = [] # list to hold questions that haven't been asked
        for question in all_qs:
            if question not in self.asked_questions[theme]:
                new_qs.append(question) 
        chosen = random.choice(new_qs) # pick one randomly from unused questions
        self.asked_questions[theme].add(chosen) # mark it as asked
        return chosen, self.qa_dict[theme][chosen] # return question and its answer

