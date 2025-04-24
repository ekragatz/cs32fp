### cs32_fp/game.py
import random
from team import Team

# Open and read the file
qa_dict = {}
teams = []

def get_question_list(file_name):
    #open and read file
    with open('example_questions.txt', 'r') as file:
        lines = file.readlines()

    # store lines in dictionary
    for i in range(0, len(lines), 2):
        question= lines[i].strip()[3:]
        answer = lines[i+1].strip()[3:]
        qa_dict[question] = answer

def ask_trivia_question(team_num):
    print(f"{teams[team_num].name} will go!")

    #generate random question
    random_q = random.choice(list(qa_dict.keys()))
    correct_a = qa_dict[random_q].lower()

    #ask the random question to choosen team
    a_given = input(random_q).strip().lower()

    if a_given == correct_a:
        print("Correct!")
        #increase team's score
        teams[team_num].add_points(1)
    else:
        print(f"Incorrect. The correct answer was {correct_a}.")

def ending_message():
    print("Thank you for playing trivia!")

    team_1 = teams[0]
    score_1 = team_1.score
    team_2 = teams[1]
    score_2 = team_2.score

    if score_1 > score_2:
        print(f"{team_1.name} won by {score_1 - score_2} points!")
    elif score_2 > score_1:
        print(f"{team_2.name} won by {score_2 - score_1} points!")
    else:
        print(f"It's a tie! Both teams have {score_1} points.")

def main():
    print("Welcome to Trivia!")

    #for our example, can change this later
    print("We will play best of 5!")

    #populate dictionary of questions
    get_question_list('example_questions.txt')

    #for our sample, will do 2 teams
    team_1 = input("Enter the first team name ")
    team_2 = input("Enter the second team name ")
    teams.extend([Team(team_1), Team(team_2)])

    random_number = random.randint(0, len(teams) - 1)
    while teams[0].score < 3 and teams[1].score < 3:
        ask_trivia_question(random_number)
        random_number = (random_number + 1) % 2

    ending_message()

if __name__ == '__main__':
    main()

