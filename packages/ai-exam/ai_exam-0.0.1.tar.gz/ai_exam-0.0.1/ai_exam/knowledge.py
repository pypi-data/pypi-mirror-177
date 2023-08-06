def knowledge():
    print('''
import itertools


class Sentence():

    def evaluate(self, model):
        """Evaluates the logical sentence."""
        raise Exception("nothing to evaluate")

    def formula(self):
        """Returns string formula representing logical sentence."""
        return ""

    def symbols(self):
        """Returns a set of all symbols in the logical sentence."""
        return set()

    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("must be a logical sentence")

    @classmethod
    def parenthesize(cls, s):
        """Parenthesizes an expression if not already parenthesized."""
        def balanced(s):
            """Checks if a string has balanced parentheses."""
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0
        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])
        ):
            return s
        else:
            return f"({s})"


class Symbol(Sentence):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            raise EvaluationException(f"variable {self.name} not in model")

    def formula(self):
        return self.name

    def symbols(self):
        return {self.name}


class Not(Sentence):
    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def formula(self):
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self):
        return self.operand.symbols()


class And(Sentence):
    def __init__(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts

    def __repr__(self):
        conjunctions = ", ".join(
            [str(conjunct) for conjunct in self.conjuncts]
        )
        return f"And({conjunctions})"

    def add(self, conjunct):
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)

    def evaluate(self, model):
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def formula(self):
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " ∧ ".join([Sentence.parenthesize(conjunct.formula())
                           for conjunct in self.conjuncts])

    def symbols(self):
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])


class Or(Sentence):
    def __init__(self, *disjuncts):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __repr__(self):
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def evaluate(self, model):
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self):
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∨  ".join([Sentence.parenthesize(disjunct.formula())
                            for disjunct in self.disjuncts])

    def symbols(self):
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])


class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other):
        return (isinstance(other, Implication)
                and self.antecedent == other.antecedent
                and self.consequent == other.consequent)

    def __repr__(self):
        return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model):
        return ((not self.antecedent.evaluate(model))
                or self.consequent.evaluate(model))

    def formula(self):
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self):
        return set.union(self.antecedent.symbols(), self.consequent.symbols())


class Biconditional(Sentence):
    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (isinstance(other, Biconditional)
                and self.left == other.left
                and self.right == other.right)

    def __repr__(self):
        return f"Biconditional({self.left}, {self.right})"

    def evaluate(self, model):
        return ((self.left.evaluate(model)
                 and self.right.evaluate(model))
                or (not self.left.evaluate(model)
                    and not self.right.evaluate(model)))

    def formula(self):
        left = Sentence.parenthesize(str(self.left))
        right = Sentence.parenthesize(str(self.right))
        return f"{left} <=> {right}"

    def symbols(self):
        return set.union(self.left.symbols(), self.right.symbols())


def model_check(knowledge, query):
    """Checks if knowledge base entails query."""

    def check_all(knowledge, query, symbols, model):
        """Checks if knowledge base entails query, given a particular model."""

        # If model has an assignment for each symbol
        if not symbols:

            # If knowledge base is true in model, then query must also be true
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:

            # Choose one of the remaining unused symbols
            remaining = symbols.copy()
            p = remaining.pop()

            # Create a model where the symbol is true
            model_true = model.copy()
            model_true[p] = True

            # Create a model where the symbol is false
            model_false = model.copy()
            model_false[p] = False

            # Ensure entailment holds in both models
            return (check_all(knowledge, query, remaining, model_true) and
                    check_all(knowledge, query, remaining, model_false))

    # Get all symbols in both knowledge and query
    symbols = set.union(knowledge.symbols(), query.symbols())

    # Check that knowledge entails query
    return check_all(knowledge, query, symbols, dict())

rain=Symbol("rain")
hagrid=Symbol("hagrid")
dumbledore=Symbol("dumbledore")
knowledge=And(Implication(Not(rain),hagrid),
             Or(hagrid,dumbledore),
             Not(And(hagrid,dumbledore)),
             dumbledore)
print(model_check(knowledge,rain))
              
mustard=Symbol("mustard")
plum=Symbol("plum")
scarlet=Symbol("scarlet")
ballroom=Symbol("ballroom")
kitchen=Symbol("kitchen")
library=Symbol("library")
knife=Symbol("knife")
revolver=Symbol("revolver")
wrench=Symbol("wrench")
people=[mustard,plum,scarlet]
rooms=[ballroom,kitchen,library]
weapons=[knife,revolver,wrench]
symbols=people+rooms+weapons

knowledge=And(
Or(mustard,plum,scarlet),
    Or(ballroom,kitchen,library),
    Or(knife,revolver,wrench),
    Not(plum),
    Or(Not(scarlet),Not(library),Not(revolver)),
    )
def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge,symbol):
            print(f'{symbol}:yes')
        elif model_check(knowledge,symbol)==False:
            print(f'{symbol}:maybe')


check_knowledge(knowledge)

knowledge.add(Not(mustard))
knowledge.add(Not(kitchen))
knowledge.add(Not(revolver))
knowledge.add(Not(ballroom))
knowledge.add(Not(wrench))

check_knowledge(knowledge)

houses=['gryffindor','slytherin','hufflepuff','ravenclaw']
people=['gilderoy','minerva','pomona','horace']
symbols=[]
knowledge_base2=And()
for p in people:
    for h in houses:
        symbols.append(Symbol(f'{p}{h}'))
for p in people:
    knowledge_base2.add(Or
                        (Symbol(f'{p}gryffindor'),
                        Symbol(f'{p}slytherin'),
                        Symbol(f'{p}hufflepuff'),
                        Symbol(f'{p}ravenclaw'))
                       )
for p in people:
    for h1 in houses:
        for h2 in houses:
            if h1!=h2:
                knowledge_base2.add(Implication
                                   (Symbol(f'{p}{h1}'),
                                        Not(Symbol(f'{p}{h2}')))
                                   )
for h in houses:
    for p1 in people:
        for p2 in people:
            if p1!=p2:
                knowledge_base2.add(Implication
                                   (Symbol(f'{p1}{h}'),
                                        Not(Symbol(f'{p2}{h}')))
                                   )
knowledge_base2.add(Not(Symbol('pomonaslytherin')))
knowledge_base2.add(Symbol('minervagryffindor'))
knowledge_base2.add(Or(Symbol('gilderoygryffindor'),Symbol('gilderoyravenclaw')))
for symbol in symbols:
    if model_check(knowledge_base2,symbol):
        print(symbol)

color=['red','blue','green','yellow']
position=['first','second','third','fourth']
symbols=[]
knowledge_base3=And()
for c in color:
    for p in position:
        symbols.append(Symbol(f'{c}{p}'))

for c in color:
    knowledge_base3.add(Or(Symbol(f'{c}first'),
                  Symbol(f'{c}second'),
                  Symbol(f'{c}third'),
                  Symbol(f'{c}fourth')))
for c in color:
    for p1 in position:
        for p2 in position:
            if p1!=p2:
                knowledge_base3.add(Implication(Symbol(f'{c}{p1}'),Not(Symbol(f'{c}{p2}'))))
for p in position:
    for c1 in color:
        for c2 in color:
            if c1!=c2:
                knowledge_base3.add(Implication(Symbol(f'{c1}{p}'),Not(Symbol(f'{c2}{p}'))))
knowledge_base3.add(Or(
And(Symbol('redfirst'),Symbol('bluesecond')),
   And(Symbol('redfirst'),Symbol('greenthird')),
    And(Symbol('redfirst'),Symbol('yellowfourth')),
    And(Symbol('bluesecond'),Symbol('greenthird')),
    And(Symbol('bluesecond'),Symbol('yellowfourth')),
    And(Symbol('greenthird'),Symbol('yellowfourth'))))

knowledge_base3.add(And(Not(Symbol('bluefirst')),Not(Symbol('redsecond')),Not(Symbol('greenthird')),Not(Symbol('yellowfourth'))))
for symbol in symbols:
    if model_check(knowledge_base3,symbol):
        print(symbol)

Aknight=Symbol('A is a knight')
Aknave=Symbol('A is a knave')
Bknight=Symbol('B is a knight')
Bknave=Symbol('B is a knave')
Cknight=Symbol('C is a knight')
Cknave=Symbol('C is a knave')
symbols=[Aknight,Aknave,Bknight,Bknave,Cknight,Cknave]
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge_base=And(
Or(Aknight,Aknave),
    Not(And(Aknight,Aknave)),
    Or(Bknight,Bknave),
    Not(And(Bknight,Bknave)),
    Or(Cknight,Cknave),
    Not(And(Cknight,Cknave)),
    Implication(Aknight,And(Aknight,Aknave)),
    Implication(Aknave,Not(And(Aknight,Aknave)))
)
for symbol in symbols:
    if model_check(knowledge_base,symbol):
        print(symbol)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge_base2=And(
Or(Aknight,Aknave),
    Not(And(Aknight,Aknave)),
    Or(Bknight,Bknave),
    Not(And(Bknight,Bknave)),
    Or(Cknight,Cknave),
    Not(And(Cknight,Cknave)),
    Implication(Aknight,And(Aknave,Bknave)),
    Implication(Aknave,Not(And(Aknave,Bknave))))

for symbol in symbols:
    if model_check(knowledge_base2,symbol):
        print(symbol)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge_base3=And(
Or(Aknight,Aknave),
    Not(And(Aknight,Aknave)),
    Or(Bknight,Bknave),
    Not(And(Bknight,Bknave)),
    Or(Cknight,Cknave),
    Not(And(Cknight,Cknave)),
  Implication(Aknight,Or(And(Aknight,Bknight),And(Aknave,Bknave))),
Implication(Aknave,Not(Or(And(Aknight,Bknight),And(Aknave,Bknave)))),
 Implication(Bknight,Or(And(Aknight,Bknave),And(Aknave,Bknight))),
    Implication(Bknave,Not(Or(And(Aknight,Bknave),And(Aknave,Bknight))))
)

for symbol in symbols:
    if model_check(knowledge_base3,symbol):
        print(symbol)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge_base4=And(
Or(Aknight,Aknave),
    Not(And(Aknight,Aknave)),
    Or(Bknight,Bknave),
    Not(And(Bknight,Bknave)),
    Or(Cknight,Cknave),
    Not(And(Cknight,Cknave)),
    Implication(Aknight,Or(Aknight,Aknave)),
    Implication(Aknave,Not(Or(Aknight,Aknave))),
    Implication(Bknight,Implication(Aknight,Bknave)),
    Implication(Bknave,Implication(Aknave,Not(Bknave))),
    Implication(Bknight,Cknave),
    Implication(Bknave,Cknight),
    Implication(Cknight,Aknight),
    Implication(Cknave,Not(Aknight))

)

for symbol in symbols:
    if model_check(knowledge_base4,symbol):
        print(symbol)
''')

knowledge()