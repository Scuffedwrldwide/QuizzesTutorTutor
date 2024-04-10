import os
import random
import re
import sys

def load_questions(folder_path):
    questions = []
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return questions
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if len(lines) % 5 != 0:
                    print(f"Invalid file format: {filename}")
                    continue
                for i in range(0, len(lines), 5):
                    question_data = {}
                    question_data['question'] = re.sub(r'^\d+\.', '', lines[i]).strip()
                    options = [line.strip() for line in lines[i+1:i+5] if line.strip()]
                    for i in range(0, len(options), 1):
                        if options[i][1] == '!':
                            options[i] = options[i].replace('!', ')', 1)
                            question_data['correct_option'] = ord(options[i][0].lower()) - ord('a')
                            break
                    question_data['options'] = options
                    questions.append(question_data)       
    return questions

def print_question(question, flag, selected_option=-1):
    print(f"\033[1m{question['question']}\033[0m\n")
    for i in range(0, len(question['options'])):
        if flag: 
            if i == question['correct_option']:
                print(f"\033[1m\033[92m    {question['options'][i]}\033[0m")
            elif i == selected_option:
                print(f"\033[1m\033[91m    {question['options'][i]}\033[0m")
            else:
                print("    " + question['options'][i])
        else: 
            print("    " + question['options'][i])
    print()

def flashcard_mode(questions):
    while True:
        current = random.choice(questions)
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.flush()
        print_question(current, False)
        answer = input("Your answer: ")
        if answer.lower() == 'q':
            break
        while re.match(r'^[a-d]$', answer, re.IGNORECASE) is None:
            print("Invalid input. Please enter a letter from a to d.")
            answer = input("Your answer: ")
            sys.stdout.write('\033[F\033[F')
            sys.stdout.write('\033[K')
        answer = ord(answer.lower()) - ord('a')
        if answer == current['correct_option']:
            print("\33[1m\33[92mCorrect!\33[0m")
        else:
            print(f"\33[1m\33[91mIncorrect!\33[0m The correct answer is: \033[1m\033[92m{chr(current['correct_option'] + ord('a'))}\33[0m")
        next = input("Press any key to continue...")
        if next == 'q':
            break

def lookup_mode(questions):
    while True:
        lookup = input("Enter a search term: ")
        found = False
        for question in questions:
            if lookup.lower() in question['question'].lower():
                found = True
                print_question(question, True)
        if not found:
            print("No questions found.")
        next = input("Press any key to continue...")
        if next == 'q':
            break

def main():
    sys.stdout.flush()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\33[1mWelcome to Quizzes Tutor Tutor! Let's get started.\33[0m\n\nFilepath:")
    folder_path = input()
    questions = load_questions(folder_path)

    if not questions:
        print("No questions found in the specified folder.")
        return
    else :
        print(f"{len(questions)} questions loaded successfully.")
        
    while True:
        sys.stdout.flush()
        os.system('cls' if os.name == 'nt' else 'clear')
        mode = input("\33[1mSelect mode:\33[0m\n\n    1. Flashcard mode\n    2. Lookup Mode\n    q. Exit\n\n")
        while mode not in ['1', '2', 'q']:
            mode = input("Invalid input. Please enter 1, 2 or q.\n")
            sys.stdout.write('\033[F\033[F')
            sys.stdout.write('\033[K')

        if mode == 'q':
            return
        elif mode == '1':
            flashcard_mode(questions)

        else:
            lookup_mode(questions)

if __name__ == "__main__":
    main()
