
def get_keyboard_bool(question : str) -> bool:
    """!Asks a question and returns True if the answer is 'y' and False if the answer is 'n'
    @param question: question to ask the user

    @return True if the answer is 'y', False if the answer is 'n', exits with code 1 otherwise
    """
    answer = input(question)
    answer = answer.strip().lower()
    if answer == 'y':
        return True
    elif answer == 'n':
        return False
    else:
        print("Only 'y' or 'n' is accepted.")
        exit(1)
