from gensim.models import KeyedVectors
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pandas as pd
import random

wv: KeyedVectors = KeyedVectors.load('../data/word2vec.wordvectors', mmap='r')
tsne = TSNE()

print(len(wv.index_to_key))
# Visiualize selected words from vocab
vocab = [
    'witch',
    'magic',
    'mana',
    'woman',
    'man',
    'girl',
    'boy',
    'king',
    'queen',
    'cat',
    'dog',
    'deer',
    'wood',
    'fire',
    'water',
    'wind',
    'sorcerer',
    'magician',
    'knight',
    'house',
    'city',
    'town',
    'husband',
    'wife',
    'nurse',
    'doctor',
    'demon',
    'vampire',
    'dungeon',
    'sea',
    'lake',
    'sky',
    'dirt',
    'skirt',
    'tunic',
    'pants',
    'hair',
    'eyes',
    'nose',
    'mouth',
    'ear',
]
X = wv[vocab]
tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)
df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.scatter(df['x'], df['y'])
for word, pos in df.iterrows():
    ax.annotate(word, pos)

plt.show()