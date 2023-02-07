def get_digit(prompt=""):
    user_input = input(prompt)
    if user_input.isdigit():
        return int(user_input)
    return ''
