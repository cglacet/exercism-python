def append_action(action_name):
    return lambda actions : actions+[action_name]

def reverse_actions():
    return lambda actions : actions[::-1]

HANDSHAKE_CODE = [
    append_action("wink"),
    append_action("double blink"),
    append_action("close your eyes"),
    append_action("jump"),
    reverse_actions()
]

def handshake(code):
    actions = []
    for i in range(len(HANDSHAKE_CODE)):
        if (code & (2**i)) > 0:
            actions = HANDSHAKE_CODE[i](actions)
    return actions

def secret_code(actions):
    pass
