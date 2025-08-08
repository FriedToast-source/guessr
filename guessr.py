from rich.console import Console
from random import randrange
import time
from prettytable import PrettyTable
import os
import json
from operator import itemgetter

console = Console()
def random():
    return (int)(randrange(1,100))

def game(randomno,difficulty):
    start_time = time.time()
    try:

        hint_taken=False
        tries=[10,5,3]
        for i in range(0,tries[difficulty-1]):
            guess = int(input("enter your guess: "))
            if guess == randomno:
                console.print(f"[green]Congratulations! You guessed the correct number in {i+1} attempts.[/green]")
                run_time = timer(start_time)
                print(f"time: {time.strftime("%H:%M:%S",time.gmtime(run_time))}")
                write_history(i,run_time,difficulty)
                show_history()

                ch = input("want to continue? (y/n)")
                if ch in ["y","Y"]:
                    game(random(),difficulty)
                else:
                    handle_game()

                return

            elif guess > randomno:
                console.print(f"[red]Incorrect! The number is less than {guess}.[/red]")

                if i in [2,3,8]:
                    hint_take = input("do you want a hint> (y/n)")
                    if hint_take in ["y","Y"] and hint_taken == False:
                        hint(randomno)
                    else:
                        continue

            elif guess < randomno:
                console.print(f"[red]Incorrect! The number is more than {guess}.[/red]")

                if i in [2,3,8]:
                    hint_take = input("do you want a hint> (y/n)")
                    if hint_take in ["y","Y"] and hint_taken == False:
                        hint(randomno,guess)
                    else:
                        continue

            else:
                console.print(f"[red]invalid input[/red]")
        else:
            console.print("[red]you lose![/red]")
            ch = input("want to continue? (y/n)")
            if ch in ["y","Y"]:
                game(random(),difficulty)
            else:
                handle_game()

    except ValueError:
        print("Invalid input. Please enter a valid integer between 1-100.")
        return

def timer(start_time):
    end_time = time.time()
    run_time = end_time - start_time


    return run_time

def write_history(tries,time,difficulty):
    level=["Easy","Medium","Hard"]
    new_data = {
    "rank":0,
    "tries":tries+1,
    "time":time,
    "difficulty":level[difficulty-1]
    }

    if not os.path.exists('highscores.json'):
        return
    with open('highscores.json', 'r+') as file:
        data = json.load(file)
        data["scores"].append(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)
    sort_history()

def show_history():
    if not os.path.exists('highscores.json'):
        return

    with open('highscores.json', 'r') as file:
        data = json.load(file)
        if len(data["scores"])>5:
            for i in range(5,len(data["scores"])):
                data["scores"].pop()

        new_data={"scores":[]}
        i=0
        for score in data["scores"]:
            new_data["scores"].append(score)
            s=time.gmtime(data["scores"][i]["time"])
            new_data["scores"][i]["time"]=time.strftime("%H:%M:%S",s)
            i+=1
        print(table(new_data["scores"]))
        return
    file.seek(0)
    json.dump(data, file, indent=4)

def sort_history():
    if not os.path.exists('highscores.json'):
        return
    with open('highscores.json', 'r+') as file:
        data = json.load(file)
        new_list={"scores":[]}
        new_list["scores"] = sorted(data["scores"], key=itemgetter('time','tries'))
        for i in range(len(data["scores"])):
            new_list["scores"][i]["rank"]=i+1


        file.seek(0)
        json.dump(new_list, file, indent=4)


def table(list):
    x = PrettyTable()
    x.field_names = ["RANK","TRIES","TIME","DIFFICULTY"]
    for item in list:
        x.add_row(item.values())
    return x

def hint(random):
    factors=0
    if random == 23:
        print("its my dogs birthyear")
        return
    else:
        for i in range(2,random):
            if random%i == 0:
                factors+=1
                print(f"its a multiple of {i}")
                return
        if factors!=1:
                print("its a prime number")
                return

def handle_game():
    while True:
        try:

            print("Please select the difficulty level: \n 1. Easy (10 chances) \n 2. Medium (5 chances) \n 3. Hard (3 chances)\n 4. history \n 5. exit")
            choice = int(input("enter your choice: "))
            choice_opt = ["Easy","Medium","Hard"]

            if choice in [1,2,3]:
                console.print(f"[green]Great! You have selected the {choice_opt[choice-1]} difficulty level.[/green]")
                console.print("[yellow]Let's start the game![/yellow]")
                randomno = random()
                game(randomno,choice)
            elif choice == 4:
                show_history()
            elif choice == 5:
                console.print("[red]Exiting.....[/red]")
                raise SystemExit("until we meet again...")
            else:
                console.print("[yellow]error, accepted values=1,2,3,4[/yellow]")
                break

        except ValueError:
            print("Invalid input. Please enter a valid integer between 1-100.")
            raise SystemExit("until we meet again...")

        except (KeyboardInterrupt, EOFError):
            console.print("[red]\nExiting.....[/red]")
            raise SystemExit("until we meet again...")

def main():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    handle_game()




if __name__ == "__main__":
    main()

