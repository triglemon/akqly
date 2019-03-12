# Two question types: Questions based on information given in the text and
# questions based on keywords (For future continuation)
from textblob import TextBlob


class WordType:
    def __init__(self, tags, recursive=False):
        self.tags = tags
        self.recursive = recursive


NOUN = WordType(('NN', 'NNS', 'NNP', 'NNPS'), True)
PRONOUN = WordType(('PRP',))
ADJECTIVE = WordType(('JJ', 'JJR', 'JJS', 'PRP$'), True)
PREPOSITION = WordType(('IN',))
DETERMINER = WordType(('PDT', 'DT'), True)
VERB = WordType(('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',), True)
ADVERB = WordType(('RB', 'RBR', 'RBS', 'WRB'), True)


class Node:
    def __init__(self, cargo=None, parents=None):
        self.cargo = cargo
        self.daughters = []
        self.parents = parents
        for parent in parents:
            parent.add_daughter(self)

    def add_daughter(self, daughter):
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

    def iterate(self):
        try:
            tag = self.tags[self.pos]
            return tag
        except IndexError:
            return None

class ClauseGraph:
    def __init__(self):
        preposition_1 = Node(PREPOSITION)
        determiner_1 = Node(DETERMINER, [preposition_1])
        adjective_1 = Node(ADJECTIVE, [determiner_1])
        noun_1 = Node(ADJECTIVE, [adjective_1])
        pronoun_1 = Node(PRONOUN, [preposition_1])
        adverb_1 = Node(ADVERB, [noun_1, pronoun_1])
        verb = Node(VERB, [adverb_1])
        preposition_2 = Node(PREPOSITION, [verb])
        determiner_2 = Node(DETERMINER, [preposition_2])
        adjective_2 = Node(ADJECTIVE, [determiner_2])
        noun_2 = Node(NOUN, [adjective_2])
        pronoun_2 = Node(PRONOUN, [preposition_2])
        adverb_2 = Node(ADVERB, [preposition_2])
        adjective_3 = Node(ADJECTIVE, [adverb_2])

        self.head = self.current = preposition_1
        self.tails = [noun_2, pronoun_2, adjective_3]
        self.clause = []

    def clause(self):
        old_clause = self.clause
        self.clause = []
        return old_clause
"""FIX"""
    def iterate(self):
        self.current = self.current.daughters
        return
        elif len(self.current.daughters) == 1:
            self.current = self.current.daughters[0]
        else:

"""FIX"""
    def process(self, sentence):
        sentence = Sentence(sentence)
        while True:
            sentence_tag = sentence.iterate()
            if not sentence_tag:
                sentence.clauses.append(self.clause)
                return
            self.iterate()

            if not clause_tags:
                self.clauses.append(clause)
                clause = Clause()
                clause_tags = clause.tag_iterate()
            if tag[1] in self.current.cargo.tags:
                self.clause.tags.append(tag)
            else:
                clause.pos += 1

    def regurg(self):
        for clause in self.clauses:
            print(clause.tags)

# Parse sentences in string
def parse_sentences(string):
    txt = TextBlob(string)
    for sentence in txt.sentences:
        ClauseGraph.process(sentence)


clause_graph = ClauseGraph()


def main():
    with open('notes2', encoding="utf8") as file:
        notes = file.read()
    parse_sentences(notes)


if __name__ == '__main__':
    main()
