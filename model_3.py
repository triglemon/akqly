# Two question types: Questions based on information given in the text and
# questions based on keywords (For future continuation)
from textblob import TextBlob


class WordType:
    def __init__(self, tags, recursive=False):
        self.tags = tags
        self.recursive = recursive


class Node:
    def __init__(self, cargo=None, parent=None):
        self.cargo = cargo
        self.daughters = []
        parent.add_daughter(self)

    def add_daughter(self, daughter):
        self.daughters.append(daughter)


class ClauseTree:
    def __init__(self):
        preposition = Node(PREPOSITION)
        determiner = Node(DETERMINER, preposition)
        adjective = Node(ADJECTIVE, determiner)
        noun = Node(ADJECTIVE, adjective)
        pronoun = Node (PRONOUN, preposition)


NOUN = WordType(('NN', 'NNS', 'NNP', 'NNPS'), True)
PRONOUN = WordType(('PRP',))
ADJECTIVE = WordType(('JJ', 'JJR', 'JJS', 'PRP$'), True)
PREPOSITION = WordType(('IN',))
DETERMINER = WordType(('PDT', 'DT'), True)
VERB = WordType(('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',), True)
ADVERB = WordType(('RB', 'RBR', 'RBS', 'WRB'), True)


class Clause:
    def __init__(self):
        self.pattern = (PREPOSITION,
                        DETERMINER,
                        ADJECTIVE,
                        NOUN,
                        PRONOUN,
                        ADVERB,
                        VERB,
                        PREPOSITION,
                        DETERMINER,
                        ADJECTIVE,
                        NOUN, 
                        PRONOUN,
                        ADVERB,
                        ADJECTIVE)
        self.tags = []
        self.pos = 0

    def __str__(self):
        return " ".join([tag[0] for tag in self.tags])

    def tag_iterate(self):
        try:
            tag = self.pattern[self.pos]
            return tag
        except IndexError:
            return None


class Sentence:
    def __init__(self, sentence):
        self.sentence = sentence
        self.tags = sentence.tags
        # Current index position in words list
        self.pos = 0
        self.clauses = []

    def tag_iterate(self):
        try:
            tag = self.tags[self.pos]
            return tag
        except IndexError:
            return None

    def process(self):
        clause = Clause()
        while True:
            sentence_tag = self.tag_iterate()
            clause_tags = clause.tag_iterate()
            if not sentence_tag:
                self.clauses.append(clause)
                return
            if not clause_tags:
                self.clauses.append(clause)
                clause = Clause()
                clause_tags = clause.tag_iterate()
            if sentence_tag[1] in clause_tags.tags:
                clause.tags.append(sentence_tag)
                self.pos += 1
            else:
                clause.pos += 1

    def regurg(self):
        for clause in self.clauses:
            print(clause.tags)


# Parse sentences in string
def parse_sentences(string):
    txt = TextBlob(string)
    for sentence in txt.sentences:
        s_map = Sentence(sentence)
        s_map.process()
        s_map.regurg()

def main():
    with open('notes2', encoding="utf8") as file:
        notes = file.read()
    parse_sentences(notes)

if __name__ == '__main__':
    main()
