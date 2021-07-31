import json
import nltk
import re
from gensim.models import Word2Vec
from nltk import tokenize
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
file = open("../get_waifu/data/waifu_details.json", "r")
details = json.loads(file.read())
sent_count = 0
corpus = []
word_regex = re.compile(r'(?:\')?[a-z]+(?:\.)?')

for obj in details:
    desc = obj['description']
    sentences = tokenize.sent_tokenize(desc)
    for sent in sentences:
        sent_count += 1
        print(f'[Sentence] {sent}')
        words = [x.lower() for x in tokenize.word_tokenize(sent)]
        print(f'[Words] {words}')
        cleaned_words = [y for y in filter(lambda x: word_regex.match(x), words)]
        print(f'[Cleaned] {cleaned_words}')
        corpus.append(cleaned_words)
        print("-------------")

print(f'Total sentences: {sent_count}')

# Train a Skip-gram word2vec model
model = Word2Vec(sentences=corpus, vector_size=100, window=5, min_count=1, workers=4, sg=1)
model.wv.save('../data/word2vec.wordvectors')
