from app.rps import determine_winner

def test_ties():
    assert determine_winner("rock", "rock") == "TIE GAME"
    assert determine_winner("paper", "paper") == "TIE GAME"
    assert determine_winner("scissors", "scissors") == "TIE GAME"

def test_user_wins():
    assert determine_winner("rock", "scissors") == "USER WINS"
    assert determine_winner("paper", "rock") == "USER WINS"
    assert determine_winner("scissors", "paper") == "USER WINS"

def test_computer_wins():
    assert determine_winner("rock", "paper") == "COMPUTER WINS"
    assert determine_winner("paper", "scissors") == "COMPUTER WINS"
    assert determine_winner("scissors", "rock") == "COMPUTER WINS"
