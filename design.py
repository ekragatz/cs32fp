### cs32_fp/design.py
import random

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
    print(f"{teams[team_num][0]} will go!")

    #generate random question
    random_q = random.choice(list(qa_dict.keys()))
    correct_a = qa_dict[random_q].lower()

    #ask the random question to choosen team
    a_given = input(random_q).strip().lower()

    if a_given == correct_a:
        print("Correct!")
        #increase team's score
        teams[team_num] = (teams[team_num][0], teams[team_num][1] + 1)
    else:
        print(f"Incorrect. The correct answer was {correct_a}.")

def ending_message():
    print("Thank you for playing trivia!")

    team_1, score_1 = teams[0]
    team_2, score_2 = teams[1]

    if score_1 > score_2:
        print(f"{team_1} won by {score_1 - score_2} points!")
    elif score_2 > score_1:
        print(f"{team_2} won by {score_2 - score_1} points!")
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
    teams.extend([(team_1, 0), (team_2, 0)])

    random_number = random.randint(0, len(teams) - 1)
    while teams[0][1] < 3 and teams[1][1] < 3:
        ask_trivia_question(random_number)
        random_number = (random_number + 1) % 2

    ending_message()

if __name__ == '__main__':
    main()
