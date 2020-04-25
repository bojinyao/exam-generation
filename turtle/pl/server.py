import random, copy
import numpy as np

try:
    import prairielearn as pl
except:
    pass
try:
    import turtle
except:
    pass

r, q, ans = 0, 0, 0
def generate(data):
    global r, q, ans
    # Put these two integers into data['params']
    data['params']['a'] = 1
    data['params']['b'] = 2

    r = MrRoboto(3)
    q = r.get_random_question()
    ans = r.get_solution_matrix(q)
    data['params']['question'] = str(q).lstrip('\n\t')

    # Answer to each matrix entry converted to JSON
    data['correct_answers']['matrixA'] = pl.to_json(ans)

# def grade(data):
#     # All elements will have already graded their answers (if any) before this point.
#     # data["partial_scores"][NAME] is the individual element scores (0 to 1).
#     # data["score"] is the total score for the question (0 to 1).
#     # We can modify or delete any of these if we have a custom grading method.
#     # This function only runs if `parse()` did not produce format errors, so we can assume all data is valid.

#     # grade() can also set `data['format_errors'][NAME]` if there is any reason to mark the question
#     # invalid during grading time.  This will cause the question to not use up one of the student's attempts' on exams.

#     # As an example, we will give half points for incorrect answers larger than "x":
#     # if data["score"] == 0: # only if not already correct
#     #     if data["submitted_answers"]["y"] > data["params"]["x"]:
#     #         data["partial_scores"]["y"] = 0.5
#     #         data["score"] = 0.5
#     print(data["submitted_answers"]["_files"])

TURN = 1
FOR_LOOP = 3
MOVE = 5

class MrRoboto:

    def __init__(self, size = 5):
        self.size = size
        self.generic_questions = []
        self.questions = []

    def constructAQuestion(self, choice_number_index, choices, prompt_arg):
        return {
            "prompt" : self.config["prompt"].format(prompt_arg),
            "choices" : choices,
            "answers" : choice_number_index
        }

    def constructQuestions(self):
        num_questions = self.config["num_questions"]
        choices = self.config["choice_numbers"][:]
        if self.config["include_none_of_the_above"]:
            choices.append("None of the above")

        assert num_questions <= len(choices)

        questions = []
        
        picked_answers = random.sample(range(len(choices)), num_questions)
        for i in range(num_questions):
            cur_answer = picked_answers[i]
            c = [(choices[i], i == cur_answer) for i in range(len(choices))]
            if self.config["shuffle_choices"]:
                random.shuffle(c)
            cur_answer = [i for i in range(len(c)) if c[i][1]][0]
            c = [pair[0] for pair in c]
            
            if type(c[cur_answer]) is int:
                questions.append(self.constructAQuestion(cur_answer, c, int(100/c[cur_answer])))
            else:
                while True:
                    n = random.randrange(5, 96, 5)
                    if n not in c:
                        questions.append(self.constructAQuestion(cur_answer, c, int(100/n)))
                        break
        return {
            "multiple_choice" : questions
        }

    def constructQuestion(self, generic, params):
        loop_bounds, move, degrees = params
        question = []
        for statement in generic.body:
            statement = statement.copy()
            if isinstance(statement, ForLoop):
                statement.bounds = loop_bounds
                statement.statements = self.constructQuestion(statement.statements, params)
            elif isinstance(statement, Move):
                statement.amount = move
            elif isinstance(statement, Turn):
                statement.degrees = degrees
            question.append(statement)

        return Statements(question)

    def constructQuestions(self):
        self.constructGenericQuestions()
        TURNS = [90, 180, -90]
        MOVES = [1,2,3,-1,-2,-3]
        FOR_LOOP = [(0, '1'), (0, '2'), (0, '3')]

        combinations = [(loop_bounds, move, turn) for loop_bounds in FOR_LOOP \
        for move in MOVES for turn in TURNS]
        questions = []
        for question in self.generic_questions:
            for combination in combinations:
                q = self.constructQuestion(question, combination)
                questions.append(q)

        return questions

    def constructGenericQuestions(self):
        inputVals = [TURN, FOR_LOOP, MOVE]
        permutations = [[self.getEmptyStatement(statement) for statement in perm] for perm in self.perms(inputVals) if self.valid_perm(perm)]
        questions = []
        for perm in permutations:
            if self.valid_perm(perm):
                for i in range(len(perm)):
                    if isinstance(perm[i], ForLoop):
                        questions += self.createForLoops(i, perm)
                        break
        self.generic_questions = questions
        return questions

    def createForLoops(self, index, question):
        output = []
        for j in range(index + 2, len(question) + 1):
            before_loop = question[0:index]
            loop = question[index].copy()
            loop.statements = Statements(question[index + 1: j])
            after_loop = question[j:]
            output.append(Statements(before_loop + [loop] + after_loop))
        return output

    def getEmptyStatement(self, statement_type):
        if statement_type == FOR_LOOP:
            return ForLoop()
        if statement_type == TURN:
            return Turn()
        if statement_type == MOVE:
            return Move()

    def valid_perm(self, perm):
        return perm[-1] != FOR_LOOP

    def perms(self, lst):
        if lst == []:
            return [[]]
        out = []
        for i in range(len(lst)):
            for perm in self.perms(lst[:i] + lst[i + 1:]):
                out += [[lst[i]] + perm]
        return out

    def valid_questions(self):
        lst = self.constructQuestions()
        questions = []
        for question in lst:
            if Matrix(self.size).is_valid(question):
                questions.append(question)
        return questions

    def get_random_question(self):
        questions = self.valid_questions() 
        return random.choice(questions)

    def get_solution_matrix(self, question):
        m = Matrix(self.size)
        question.execute_matrix(m)
        return m.matrix

    def execute_random_question(self):
        q = self.get_random_question()
        print("Executing:\n", q)
        # d = Drawing()
        # d.execute_question(q)
        return get_solution_matrix(q)

class Drawing:
    c = 2
    dist = 50
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.drawing_turtle = turtle.Turtle()
        self.drawing_turtle.ht()
        self.filenum = 0

    def draw_grid(self):
        dist = Drawing.dist
        c = 2
        lines = 8
        half = lines // 2
        low_pos = dist / 2 - half * dist
        turtle.tracer(0, 0)
        t = self.turtle
        for y in range(-half, half):
            t.penup()
            t.setpos(c * low_pos, c * (dist * y + dist / 2))
            t.pendown()
            t.forward(c * -2 * low_pos)
        t.left(90)
        for x in range(-half, half):
            t.penup()
            t.setpos(c * (dist * x + dist / 2), c * low_pos)
            t.pendown()
            t.forward(c * -2 * low_pos)
        t.penup()
        t.right(90)
        t.setpos(0, 0)
        t.ht()
        turtle.update()

    def execute_random_question(self):
        s = MrRoboto(5)
        import random
        lst = s.constructQuestions()
        q = random.choice(lst)
        self.execute_question(question)

    def execute_question(self, q):
        turtle.tracer(0, 0)
        drawing_turtle = self.drawing_turtle
        drawing_turtle.st()
        drawing_turtle.reset()
        drawing_turtle.color("red")
        print("Executing:\n", q)
        q.execute(self.drawing_turtle)

    def save_screen(self):
        from PIL import Image
        import tkinter
        ts = turtle.getscreen()
        ts.getcanvas().postscript(file=f"./images/{str(self.filenum)}.eps")
        Image.open(f"./images/{str(self.filenum)}.eps").save(f"./images/{str(self.filenum)}.png")
        self.filenum += 1

class Empty():

    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol

class Statements:
    def __init__(self, body = []):
        self.body = body

    def __str__(self):
        output = ""
        for statement in self.body:
            output += f"\n{str(statement)}"
        return output.lstrip('\n')

    def __repr__(self):
        return repr(self.body)

    def blank_str(self):
        output = ""
        for statement in self.body:
            output += f"\n{statement.blank_str()}"
        return output.lstrip('\n')

    def execute(self, turtle_obj):
        turtle_obj.setheading(90)
        for statement in self.body:
            statement.execute(turtle_obj)
        turtle.update()

    def execute_matrix(self, matrix):
        for statement in self.body:
            statement.execute_matrix(matrix)

class Matrix:
    def __init__(self, size = 11):
        self.matrix = np.zeros(shape = (size, size))
        self.curr_pos = (size // 2, size // 2)
        self.xdir = 0
        self.ydir = -1
        self.dir_transition = -1
        self.matrix[self.curr_pos] = 1
    
    def turn(self, degrees):
        for _ in range((degrees % 360) // 90):
            self.right_turn()
    
    def right_turn(self):
        old_xdir = self.xdir
        self.xdir = self.dir_transition * self.ydir
        self.ydir = self.dir_transition * old_xdir
        self.dir_transition *= -1 

    def forward(self, amount):
        move_dir = 1 if amount >= 0 else -1
        for _ in range(abs(amount)):
            x, y = self.curr_pos
            self.curr_pos = x + move_dir * self.xdir, y + move_dir * self.ydir
            if not self.valid_pos(self.curr_pos):
                raise IndexError
            self.matrix[self.curr_pos[::-1]] = 1

    def valid_pos(self, pos):
        if min(pos[0], pos[1]) < 0:
            return False
        if max(pos[0], pos[1]) >= len(self.matrix):
            return False
        return True

    def execute_random_question(self):
        s = MrRoboto(5)
        import random
        lst = s.constructQuestions()
        q = random.choice(lst)
        print("Executing:\n", q)
        q.execute_matrix(self)

    def is_valid(self, question):
        try:
            question.execute_matrix(self)
        except IndexError:
            return False
        return True

class ForLoop():
    """ 
    Initalize the for loop using bounds and statements

    bounds: a tuple consisting of the lower and upper bound of the for loop
    statements: an array of statements that go into the for loop
    """
    blank1 = Empty("A")
    blank2 = Empty("B")

    def __init__(self, statements = Statements(), bounds = (0, '1')):
        self.bounds = bounds
        self.statements = statements

    def __repr__(self):
        # return self.__str__()
        return f"ForLoop({self.bounds}, {repr(self.statements)})"

    def __str__(self):
        body_string = ""
        for statement in self.statements.body:
            body_string += f"\t{statement}\n"
        return f"for i = {self.bounds[0]} to {self.bounds[1]}: \n {body_string.rstrip()}"

    def blank_str(self):
        body_string = ""
        for statement in self.statements.body:
            body_string += f"\t{statement.blank_str()}\n"
        return f"for i = {self.blank1} to {self.blank2}: \n {body_string.rstrip()}"

    def copy(self):
        return ForLoop(self.statements, self.bounds)

    def execute(self, turtle_obj):
        for i in range(self.bounds[0], int(self.bounds[1]) + 1):
            for statement in self.statements.body:
                statement.execute(turtle_obj)

    def execute_matrix(self, matrix):
        for i in range(self.bounds[0], int(self.bounds[1]) + 1):
            for statement in self.statements.body:
                statement.execute_matrix(matrix)

class Move():
    blank = Empty("C")

    def __init__(self, amount = 0):
        self.amount = amount

    def __str__(self):   
        return f"forward {self.amount} steps"

    def __repr__(self):
        return f"Move({self.amount})"

    def blank_str(self):
        return f"Move({self.blank})"
    def copy(self):
        return Move(self.amount)

    @property
    def param(self):
        return self.amount

    @param.setter
    def param(self, amount):
        self.amount = amount

    def execute(self, turtle_obj):
        turtle_obj.forward(Drawing.dist * 2 * self.amount)

    def execute_matrix(self, matrix):
        matrix.forward(self.amount)


class Turn():

    blank = Empty("D")

    def __init__(self, degrees = 0):
        self.degrees = degrees

    def __str__(self):
        return f"turn {self.degrees} degrees"

    def __repr__(self):
        return f"Turn({self.degrees})"

    def blank_str(self):
        return f"turn {self.blank} degrees"

    def copy(self):
        return Turn(self.degrees)

    def execute(self, turtle_obj):
        turtle_obj.right(self.degrees)

    def execute_matrix(self, matrix):
        matrix.turn(self.degrees)
