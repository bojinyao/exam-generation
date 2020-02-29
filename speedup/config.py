from util import printErr
default_configuration = {
    "num_questions" : 1, 
    "prompt": "If {0}% of a program is serial, what's the max speedup we can get with infinite cores?",
    "numbered_choice_count" : None, # alt. int
    "choice_numbers": [5, 10, 20, 25], # alt. None
    "include_none_of_the_above": True,
    "shuffle_choices": False
}

# Update default_configuration with a new dictionary input
def update_default_config(newConfig):
    for key, val in newConfig.items():
        if key in default_configuration \
            and (val is None \
                    or default_configuration[key] is None \
                    or type(val) == type(default_configuration[key])
                    ):
            default_configuration[key] = val
        else:
            raise AssertionError(f'config: ("{key}", {val}) not recognized or value is incorrect type')
    return default_configuration
