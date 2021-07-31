# Compiles all descriptions into a single .txt file for training language models
import json
from gensim.models import KeyedVectors
from nltk import tokenize
import numpy as np
from os import path


details_file = open("../get_waifu/data/waifu_details.json", "r")
stop_words = json.loads(open('../data/stop_words.json', 'r').read())
buffer = ""
details = json.loads(details_file.read())
details_file.close()

wv: KeyedVectors = KeyedVectors.load('../data/word2vec.wordvectors', mmap='r')


def _get_rank(x, attr):
    rank = x[attr]
    if rank is None:
        return 15000
    return rank


def vectorize(descriptions, sequence_length=100):
    word_lists = [tokenize.word_tokenize(desc) for desc in descriptions]
    desc_sequences = np.full((len(descriptions), sequence_length), 0)
    for i, word_list in enumerate(word_lists):
        print(f'{i + 1} of {len(word_lists)}')
        for j in range(sequence_length):
            if j >= len(word_list):
                continue
            word = word_list[j].lower()
            if word in wv:
                desc_sequences[i, j] = wv.key_to_index[word]
    return desc_sequences


def get_waifu_dataset(sequence_length=100):
    sequences_path = '../data/desc_sequences.npy'
    if path.exists(sequences_path):
        desc_sequences = np.load(sequences_path)
    else:
        descriptions = [x['description'] for x in details]
        desc_sequences = vectorize(descriptions, sequence_length)
        np.save(sequences_path, desc_sequences)
    rank = np.array([_get_rank(x, 'like_rank') for x in details])
    rank = rank / rank.max() * 1000
    return desc_sequences, np.array(rank)


def get_gender_dataset():
    descriptions = [x['description'] for x in details]
    is_male = [x['husbando'] for x in details]
    centroids_path = '../data/desc_centroids.npy'
    if path.exists(centroids_path):
        vectors = np.load(centroids_path)
    else:
        vectors = np.zeros((len(descriptions), 100))
        for i, desc in enumerate(descriptions):
            vectors[i] = calculate_centroid_vector(desc)
        np.save(centroids_path, vectors)
    print(f'Dataset size before cleaning: {len(vectors)}')
    X, y = remove_invalid_entries(lambda x: x.sum() == 0, vectors, np.array(is_male))
    print(f'Dataset size after cleaning: {len(X)}')
    return X, y


def remove_invalid_entries(criterion, X, y):
    """
    Remove all indices from X and y with entry from X matching criterion

    :param criterion: a predicate
    :return: X, y arrays after filtering with criterion
    """
    indices = []
    for i in range(len(X)):
        if criterion(X[i]):
            indices.append(i)
    new_X = np.delete(X, indices, axis=0)
    new_y = np.delete(y, indices)
    return new_X, new_y


def calculate_centroid_vector(doc):
    """
    :param doc: input document, a paragraph of text
    :return: 100 dimensional word centroid vector of the paragraph
    """
    vectors = []
    sentences = tokenize.sent_tokenize(doc)
    for sent in sentences:
        words = [x.lower() for x in tokenize.word_tokenize(sent)]
        for word in words:
            if word in wv and word not in stop_words:
                vectors.append(wv[word])
    if len(vectors) == 0:
        print(doc)
        print('Warning: Invalid Document.')
        return np.zeros(100)
    return np.array(vectors).mean(axis=0)
