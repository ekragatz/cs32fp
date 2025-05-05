### cs32_fp/themes.py
import random

class ThemeManager:
    def __init__(self, theme_names, base_path="themed_q_a"):
        self.themes = theme_names
        self.base_path = base_path
        self.qa_dict = {}  # maps to dictionary of questions and answers
        self.asked_questions = {theme: set() for theme in theme_names} #tracks what questions have been asked
        self.load_all_themes() #loading the text files into the themes

    def load_all_themes(self):
        for theme in self.themes:
            file_path = f"{self.base_path}/{theme.replace(" ", "-")}-qa.txt"
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    qas = {}
                    for i in range(0, len(lines), 2):
                        question = lines[i].strip()[3:]
                        answer = lines[i+1].strip()[3:]
                        qas[question] = answer
                    self.qa_dict[theme] = qas
            except FileNotFoundError:
                print(f"File not found for theme '{theme}'. Skipping.")
                self.qa_dict[theme] = {}

    def get_available_themes(self):
        available = []
        for theme in self.themes:
            if len(self.asked_questions[theme]) < len(self.qa_dict[theme]):
                available.append(theme)
        return available

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
