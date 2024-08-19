import requests
import html
import random
from tkinter import *
class play_quize(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.title("Quiz")
        
#1 get a pool of trival question
def get_question(amount :int, categories : int)->list:
    url = f"https://opentdb.com/api.php?amount={amount}&category={categories}"
    response = requests.get(url)
    response_json = response.json()
    return response_json["results"]


#2 shuffle the option of question
def shuffle_choices(choices : list)->list:
    random.shuffle(choices)
    return choices

#3 print the answer choice inc onsole
def print_choices(choices : list)->None:
    for x,y in enumerate(choices):
        print(f"{x+1}.{html.unescape(y)}") # here x is choices_index and y = choice

#4 get the user choice in console
def get_user_choice(type:str)->int:
    while True:
        if type == "multiple":
            user_choice = int(input("enter the number your choice : "))
            if user_choice in range(1,5): #1,2,3,4
                return user_choice-1
            else:
                print("invalid input")
        else:
            user_choice = int(input("enter the number your choice : "))
            if user_choice in range(1, 3):  # 1,2 list[0,1]
                return user_choice - 1
            else:
                print("invalid input")


#5 play the game
def Play_Game(amount : int,category : int)->float:
    score = 0
    question_pool = get_question(amount,category) # return listr of question
    for question in question_pool:
        question_text = html.unescape(question["question"])  # question symbols in orignL FORM "@,<,>,?"
        print(question_text)  # PRINT QUESTION
        choices = question["incorrect_answers"]
        choices.extend([question["correct_answer"]])
        shuffled_choices = shuffle_choices(choices)
        print_choices(shuffled_choices)
        user_choice_index = get_user_choice(question["type"])
        user_choice_text :str  = shuffled_choices[user_choice_index]
        correct_choice_text = html.unescape(question["correct_answer"])
        if user_choice_text == correct_choice_text:
            score = score + 2
            print(f"correct ! you answered:{correct_choice_text}\n ")
        else:
            score = score - 0.5
            print(f"Wrong ! you answered:{correct_choice_text}\n ")
    return score

#call main function
"""if __name__ == "__main__":
    print("-------welcome to Quize-------")
    option = input("Do you wish to play game :").lower()
    if option == 'yes':
        print("---------RULE---------")
        print()
        allcategories = ["1.General Knowledge","2.Books","3.Film","4.Music","5.Musicals & Theatres","6.Television","7.Video Game","8.Board Game","9.Science & Nature","10.Computers"]
        for c in allcategories:
            print(c)
        categories = int(input("Enter Categories No for Quiz :"))
        amount = 10
        s = Play_Game(amount,categories+8)
        print("Thank you for appearing QUIZ")
        print("Your score is :",s,"out of 20")
    else:
        print("Ok come back soon ")
"""
if __name__ == "__main__":
    obj = play_quize()
    obj.mainloop()
