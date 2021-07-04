import math, random
from typing import List, Tuple


def start_pad(n):
    return ['~'] * n


Pair = Tuple[str, str]
Ngrams = List[Pair]


def ngrams(n, text: str) -> Ngrams:
    words = start_pad(n)
    words += text.strip().split()
    grams = []
    for i in range(n, len(words)):
        grams.append((' '.join(words[i-n:i]), words[i]))
    return grams


def add_one(counter: dict, e):
    """ Dict counter utility """
    if e in counter.keys():
        counter[e] += 1
    else:
        counter[e] = 1


def get_count(counter: dict, e):
    if e in counter.keys():
        return counter[e]
    return 0


def create_ngram_model(model_class, path, n=2, k=0):
    model = model_class(n, k)
    with open(path, encoding='utf-8') as f:
        model.update(f.read())
    return model


class NgramModel(object):

    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.vocab = set()
        self.contextCounter = {}
        self.occurrences = {}
        self.sortedV = None

    def get_vocab(self):
        return self.vocab

    def update(self, text: str):
        self.vocab = self.vocab.union({x for x in text.strip().split()})
        self.sortedV = None
        grams = ngrams(self.n, text)
        for gram in grams:
            add_one(self.occurrences, gram)
            add_one(self.contextCounter, gram[0])

    def prob(self, context: str, word: str):
        if context not in self.contextCounter:
            return 1 / len(self.vocab)
        occurrences = get_count(self.occurrences, (context, word))
        contextCount = get_count(self.contextCounter, context)
        return (occurrences + self.k) / (contextCount + self.k * len(self.vocab))

    def random_word(self, context):
        r = random.random()
        if self.sortedV is None:
            self.sortedV = list(self.vocab)
            self.sortedV.sort()
        s = 0
        for w in self.sortedV:
            s += self.prob(context, w)
            if s > r:
                return w

    def random_text(self, length):
        words = start_pad(self.n)
        while len(words) < length + self.n:
            words.append(self.random_word(' '.join(words[-self.n::])))
        return ' '.join(words[self.n::])

    def perplexity(self, text):
        s = 0
        for context, c in ngrams(self.n, text):
            p = self.prob(context, c)
            if p <= 0.0:
                return float('inf')
            s += math.log2(p)
        s /= len(text)
        return pow(2, -s)


class NgramModelWithInterpolation(NgramModel):

    def __init__(self, n, k):
        super(NgramModelWithInterpolation, self).__init__(n, k)
        self.lambdaWeights = None

    def update(self, text):
        self.vocab = self.vocab.union({x for x in text.strip().split()})
        self.sortedV = None
        for i in range(self.n + 1):
            grams = ngrams(i, text)
            for gram in grams:
                add_one(self.occurrences, gram)
                add_one(self.contextCounter, gram[0])

    def set_lambda(self, weights):
        self.lambdaWeights = weights

    def prob(self, context, word):
        if context not in self.contextCounter:
            return 1 / len(self.vocab)
        w = [1 / (self.n + 1)] * (self.n + 1) if self.lambdaWeights is None else self.lambdaWeights
        s = 0
        context_words = context.split(' ')
        for i in range(len(context_words) + 1):
            ctx = ' '.join(context_words[i::])
            occurrences = get_count(self.occurrences, (ctx, word))
            contextCount = get_count(self.contextCounter, ctx)
            s += w[i] * (occurrences + self.k) / (contextCount + self.k * len(self.vocab))
        return s


if __name__ == '__main__':
    m: NgramModel = create_ngram_model(NgramModelWithInterpolation, '../data/waifu_descriptions.txt', 4)
    print('Training finished. Generating random text.')
    while True:
        print(m.random_text(100))

