import random

VALID_OPTIONS = ["rock", "paper", "scissors"]


def determine_winner(u, c):
    if u == c:
        return "TIE GAME"

    if (
        (u == "rock" and c == "scissors")
        or (u == "paper" and c == "rock")
        or (u == "scissors" and c == "paper")
    ):
        return "USER WINS"

    return "COMPUTER WINS"


if __name__ == "__main__":
    user_choice = input("Choose rock, paper, or scissors: ").strip().lower()

    if user_choice not in VALID_OPTIONS:
        print("Invalid choice. Please run the game again.")
    else:
        computer_choice = random.choice(VALID_OPTIONS)

        print("USER:", user_choice)
        print("COMPUTER:", computer_choice)

        winner = determine_winner(user_choice, computer_choice)
        print(winner)
        
