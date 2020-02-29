import random

from computed_choices import all_valid_choices
class speedUp:

    def __init__(self, config):
        self.config = config

    def constructAQuestion(self, choice_number_index, choices, prompt_arg):
        return {
            "prompt" : self.config["prompt"].format(prompt_arg),
            "choices" : choices,
            "answers" : choice_number_index
        }

    def parseConfig(self):
        num_questions = self.config["num_questions"]

        if self.config["choice_numbers"] is not None:
            # these 2 options are mutually exclusive
            assert self.config["numbered_choice_count"] is None, 'Only 1 of "choice_numbers" and "numbered_choice_count" can be specified'

            choices = self.config["choice_numbers"][:]

        elif self.config["numbered_choice_count"] is not None:
            count = self.config["numbered_choice_count"]
            assert count <= len(all_valid_choices), f'There are only {len(all_valid_choices)} valid choices'

            choices = random.sample(all_valid_choices, count)

        else:
            raise AssertionError('1 of "choice_numbers" and "numbered_choice_count" must be specified')
            
        if self.config["include_none_of_the_above"]:
            choices.append("None of the above")

        return num_questions, choices, self.config["shuffle_choices"]

    def constructQuestions(self):
        num_questions, choices, shuffle_choices = self.parseConfig()

        questions = []
        
        picked_answers = random.sample(range(len(choices)), num_questions)
        for i in range(num_questions):
            cur_answer = picked_answers[i]
            c = [(choices[i], i == cur_answer) for i in range(len(choices))]
            if shuffle_choices:
                random.shuffle(c)
            cur_answer = [i for i in range(len(c)) if c[i][1]][0]
            c = [pair[0] for pair in c]
            
            if type(c[cur_answer]) is int:
                num = c[cur_answer]
                percentage = 100/num
                assert int(percentage) == percentage, f'Inputted number: {num} does not result in integer percentage'
                questions.append(self.constructAQuestion(cur_answer, c, int(100/num)))
            else:
                while True:
                    n = random.randrange(5, 96, 5)
                    if n not in c:
                        questions.append(self.constructAQuestion(cur_answer, c, int(100/n)))
                        break
        return {
            "multiple_choice" : questions
        }
