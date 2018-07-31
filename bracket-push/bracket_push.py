closing_match = {
    '{' : '}',
    '(' : ')',
    '[' : ']'
}
closing_elements = set(closing_match.values())

def is_matching(current_char, char_history):
    if len(char_history) == 0:
        return False
    return (closing_match[char_history.pop()] == current_char)

def is_paired(input_string):
    char_history = []
    for current_char in input_string:
        if current_char in closing_match.keys():
            char_history.append(current_char)
        elif current_char in closing_elements:
            if not is_matching(current_char, char_history):
                return False
    return len(char_history) == 0
