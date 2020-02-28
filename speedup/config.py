from util import printErr
default_configuration = {
    "num_questions" : 1, 
    "prompt": "If {0}% of a program is serial, what's the max speedup we can get with infinite cores?",
    "choice_numbers": [5, 10, 20, 25],
    "include_none_of_the_above": True,
    "shuffle_choices": True
}

# Update default_configuration with a new dictionary input
def update_default_config(config):
    for key, val in config.items():
        if key in default_configuration \
            and type(val) is type(default_configuration[key]):
            default_configuration[key] = val
        else:
            import sys
            printErr(f'config: "{key}" not recognized')
    return default_configuration
