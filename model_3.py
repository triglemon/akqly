# Two question types: Questions based on information given in the text and
# questions based on keywords (For future continuation)
from textblob import TextBlob


class WordType:
    def __init__(self, tags, recursive=False):
        self.tags = tags
        self.recursive = recursive


NOUN = WordType(('NN', 'NNS', 'NNP', 'NNPS'), True)
PRONOUN = WordType(('PRP',), True)
ADJECTIVE = WordType(('JJ', 'JJR', 'JJS', 'PRP$'), True)
PREPOSITION = WordType(('IN',))
DETERMINER = WordType(('PDT', 'DT'), True)
VERB = WordType(('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',), True)
ADVERB = WordType(('RB', 'RBR', 'RBS', 'WRB'), True)


class Node:
    def __init__(self, cargo=None, parents=None, empty=False):
        self.cargo = cargo
        self.daughters = []
        self.parents = parents
        if not empty:
            for parent in parents:
                parent.add_daughter(self)
            if self.cargo.recursive:
                self.add_daughter(self)

    def add_daughter(self, daughter):
        if daughter not in self.daughters:
            self.daughters.append(daughter)


class Clause:
    def __init__(self):
        self.tags = []

    def __str__(self):
        return " ".join([tag[0] for tag in self.tags])


class Sentence:
    def __init__(self, sentence):
        self.sentence = sentence
        self.tags = sentence.tags
        # Current index position in words list
        self.pos = 0
        self.clauses = []

    def increment(self):
        self.pos += 1

    def iterate(self):
        try:
            tag = self.tags[self.pos]
            return tag
        except IndexError:
            return None


class ClauseGraph:
    def __init__(self):
        self.head = self.current = Node(empty=True)
        preposition_1 = Node(PREPOSITION, [self.head])
        determiner_1 = Node(DETERMINER, [self.head, preposition_1])
        adjective_1 = Node(ADJECTIVE, [self.head, preposition_1, determiner_1])
        noun_1 = Node(NOUN, [self.head, adjective_1, preposition_1, determiner_1, ])
        pronoun_1 = Node(PRONOUN, [self.head, preposition_1])
        adverb_1 = Node(ADVERB, [self.head, noun_1, pronoun_1])
        verb = Node(VERB, [self.head, preposition_1, noun_1, pronoun_1, adverb_1])
        preposition_2 = Node(PREPOSITION, [verb, noun_1, ])
        determiner_2 = Node(DETERMINER, [verb, preposition_2])
        adjective_2 = Node(ADJECTIVE, [verb, preposition_2, determiner_2])
        noun_2 = Node(NOUN, [verb, preposition_2, determiner_2, adjective_2])
        pronoun_2 = Node(PRONOUN, [verb, preposition_2])
        adverb_2 = Node(ADVERB, [verb, noun_2, preposition_2])
        adjective_3 = Node(ADJECTIVE, [verb, noun_2, adverb_2])
        self.clause = []

    def regurg(self):
        old_clause = self.clause
        print(old_clause)
        self.clause = []
        self.current = self.head
        return old_clause

    def newde(self, node):
        self.current = node

    def process(self, sentence):
        sentence = Sentence(sentence)
        while True:
            sentence_tag = sentence.iterate()
            if not sentence_tag:
                sentence.clauses.append(self.regurg())
                return sentence
            successor = False
            for node in self.current.daughters:
                if sentence_tag[1] in node.cargo.tags:
                    self.clause.append(sentence_tag)
                    self.newde(node)
                    successor = True
                    break
            if not successor:
                sentence.clauses.append(self.regurg())
            else:
                sentence.increment()


def main():
    clause_graph = ClauseGraph()
    with open('comparison_notes', encoding="utf8") as file:
        notes = file.read()
    txt = TextBlob(notes)
    for sentence in txt.sentences:
        print(clause_graph.process(sentence).clauses)


if __name__ == '__main__':
    main()
