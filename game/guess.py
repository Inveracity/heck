from game.database import target_details
from game.database import state_change

def password(target):
    target_data = target_details(target)

    secret = target_data["password"]
    hidden = [char for char in secret]
    board  = ["_" for x in hidden]

    if password:
        while True:
            try:
                user_input = input("enter password: ")
                guess      = [char for char in user_input]
                pad        = len(hidden)
                trimmed    = (guess + pad * ['_'])[:pad]  # padding
                likeness   = board

                # Step through each character
                # Output all the correctly positioned characters
                for i in range(len(hidden)):
                    for c in trimmed:
                        if c in hidden[i]:
                            board[i] = c

                print(" ".join(likeness))

                if hidden == guess:
                    return True

            except KeyboardInterrupt:
                return False

    return True
