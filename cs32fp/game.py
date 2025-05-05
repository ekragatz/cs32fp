### cs32_fp/game.py
import random
from team import Team
from themes import ThemeManager

themes = ['Tennis', 'Harvard CS', 'Crimson Sports', 'Countries and Capitals', 'Famous Alumni', 'History of Women', 'Name that Movie', 'States and Capitals', 'World History', 'Famous Books', 'True or False', 'Brain Teasers']
theme_manager = ThemeManager(themes)
teams = []
max_score = 5

def opening_message():
    print("Welcome to Trivia!")
    print("We will play best of 5!")

def select_theme():
    available_themes = theme_manager.get_available_themes()
    print("Available themes:", ", ".join(available_themes))
    while True:
        theme = input("Select a theme: ").strip()
        if theme in available_themes:
            return theme
        print("Invalid theme. Please choose from the listed options.")

def ask_trivia_question(team_num, theme):
    question, correct_answer = theme_manager.get_random_question(theme)
    print(f"\nQuestion from {theme}:\n> {question}")
    answer = input("Your answer: ").strip().lower()

    if answer.strip().lower() == correct_answer.strip().lower():
        print("Correct!")
        teams[team_num].add_points(1)
    else:
        print(f"Incorrect. The correct answer was: {correct_answer}")

def ending_message():
    print("\nThank you for playing trivia!")
    team_1, team_2 = teams[0], teams[1]

    if team_1.score > team_2.score:
        print(f"{team_1.name} won by {team_1.score - team_2.score} points!")
    elif team_2.score > team_1.score:
        print(f"{team_2.name} won by {team_2.score - team_1.score} points!")
    else:
        print(f"It's a tie! Both teams have {team_1.score} points.")

def main():
    opening_message()

    # Team setup
    team_1 = input("Enter the first team name: ")
    team_2 = input("Enter the second team name: ")
    teams.extend([Team(team_1), Team(team_2)])

    # Trivia loop
    current_team = random.randint(0, 1)
    while teams[0].score < max_score and teams[1].score < max_score:
        print(f"{teams[current_team].name}, it's your turn to pick a theme.")
        theme_choice = select_theme()

        ask_trivia_question(current_team, theme_choice)
        current_team = (current_team + 1) % 2

    ending_message()

if __name__ == '__main__':
    main()
