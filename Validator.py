def is_int(number):
    try:
        int(number)
        return (True, int(number))
    except ValueError:
        return (False, 0)


def get_user_int(message):
    """Return an integer from the user
    """
    while True:
        user_input = input('{}'.format(message))
        try:
            number = is_int(user_input)[1]
            if number <= 0:
                print("Enter a positive or greater than 0")
                continue
        except ValueError:
            print('You must enter a whole number.')
            continue
        return number


def get_string1_input(string):
    while True:
        if string:
            string2 = input(string)
            return string2
        else:
            print("You must enter something")
            break


def is_whole_number(number, valid_range=None):
    try:
        number_as_int = int(number)
        if number_as_int in valid_range:
            return True

        # check if the number is in range if a range has been given
        if valid_range and number_as_int in valid_range:
            return True
        else:
            return False
    except ValueError:
        # also return False if an integer is not passed
        return False