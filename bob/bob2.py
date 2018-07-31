import re

bob_behaviour = {
    "yelled_at": {
        "question": "Calm down, I know what I'm doing!",
        "phrase": "Whoa, chill out!",
    },
    "normal_speech": {
        "question": "Sure."
    },
    "mute": "Fine. Be that way!"
}
error_message = "Whatever."

def hey(phrase):
    return bob_response(phrase)

def bob_response(phrase):
    responses = bob_responses_according_to_speech_form(phrase)
    if isinstance(responses, str):
        return responses
    else:
        phrase_type = phrase_form(phrase)
        if phrase_type in responses:
            return responses[phrase_type]
    return error_message

def bob_responses_according_to_speech_form(phrase):
    form = speech_form(phrase)
    if form in bob_behaviour:
        return bob_behaviour[form]
    else:
        return error_message

def speech_form(phrase):
    if is_yelled(phrase):
        return "yelled_at"
    if is_empty(phrase):
        return "mute"
    return "normal_speech"
def phrase_form(phrase):
    if is_question(phrase):
        return "question"
    else:
        return "phrase"

def is_yelled(phrase):
    contains_lowercase = any(c.islower() for c in phrase)
    contains_uppercase = any(c.isupper() for c in phrase)
    return not is_empty(phrase) and not contains_lowercase and contains_uppercase
def is_empty(phrase):
    return re.match(r"^\s*\Z", phrase)
def is_question(phrase):
    return re.match(r"^.*[?]\s*\Z", phrase)

