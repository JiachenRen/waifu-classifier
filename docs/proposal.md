# Proposal

Authors: Jiachen Ren, Payman Behnam, Micheal Whitaker Chu, Shashwat Shivam, Aditya Tapshalkar

## Introduction / Background

For our course project, we would be building a waifu-classifier. When given a paragraph of text describing an anime character, our classifier decides whether the description is for a waifu/husbando/trash. 

Classifiers are perhaps easiest to train compared to other machine learning models due to its simplicity - the model learns to map features from input into one of the output labels. Despite being easy to train, classifiers have a wide range of applications - a simple binary classifier can be used to identify spam emails while a more complex one can be trained to recognize digits, letters, or car models. 

Training a classifier is not hard, but choosing the right features can be a challenging task. Since our project is primarily concerned with NLP, it is indispensable to talk about the concept of word2vec. The paper by Tomas Mikolov et. al.[[1]](https://arxiv.org/abs/1301.3781) in 2013 introduced the concept of representing a word in vector space, capturing its semantic and contextual meanings, while the same team of researchers published a follow-up paper discussing several techniques including negative sampling that can be used to improve the embeddings[[2]](https://papers.nips.cc/paper/2013/file/9aa42b31882ec039965f3c4923ce901b-Paper.pdf).

Aside from word2vec, the concept of a Language Model might also become relevant. A language model is a probabilistic distribution that when sampled, spits out a sequence of words that most likely belong to the language that it is modeled after. For the unsupervised learning portion of the project, we might also consider building a Ngram or RNN based language model[[3]](https://www.isca-speech.org/archive/archive_papers/interspeech_2010/i10_1045.pdf) using our data.

## Problem Definition

Gmails, outlook, and other prominent mail providers have ML based spam detectors. Much like a spam detector, we will build our own dataset of anime characters. The metadata for each anime character we gather would contain a few paragraphs of description for the character, people’s rating of the character, and number of likes/dislikes among other things. We train a classifier using this dataset to classify any paragraph of text as either describing a waifu, a husbando, or a trash. To get our input feature, we train a word2vec embedding using gathered descriptions as training corpus. There are three labels, respectively waifu, husbando, and trash. We might also train a language model using the description from the dataset as corpus to demonstrate unsupervised learning.

## Methods

### Data Collection

To collect the necessary data for this project, we will be building a simple web scraper using the Dart language and the Puppeteer package. The scraper would scrape about 300 characters each off of the waifu, husbando, and trash lists that are hosted on https://mywaifulist.moe/, totalling to about 1000 characters (we can easily acquire more if deemed necessary). From each character’s profile, we collect the description for the character, number of likes, number of dislikes, and the ranking of the character on the lists. The collected data is stored in JSON format.

### Word2Vec Embedding (Unsupervised Learning)

Using the character’s descriptions as documents, we would train a skip-gram word2vec model with negative sampling. Alternatively, we would use a pretrained Reddit word2vec model. For each word in an input paragraph of text, the model would output a unique vector representation of the word capturing its semantics.

### Feature Selection

The only feature we would be using is a centroid of all the words in the character’s description. The centroid can be calculated by averaging the vector representation of all words. Labels are computed by comparing the character’s likes, dislikes, and gender. 

### Training and Validation

The gathered dataset would be split 8:2 for training and validation.

## Potential Results

Although we are not expecting any major problems with the implementation of the waifu-classifier, there are few minor concerns:

1. Using only the centroid as the feature can lead to a loss of a lot of information and might confound the result of classification. To address this problem, we can do a k-means clustering of word vectors and only take cluster centers as features. This amounts to feature dimension reduction and can preserve more information.

2. The specific neural network architecture to use has not yet been decided, but we are thinking of either a CNN or just linear layers. The CNN might perform better since in theory it would preserve syntactical and spatial order of words as features. 

In the end, we expect to make a high performance classifier that when given any paragraph of text that it has not seen, predicts whether the text describes a trash, waifu, or husbando.

## References

[1] T. Mikolov, K. Chen, G. Corrado, and J. Dean, “Efficient Estimation of Word Representations in Vector Space,” arXiv.org, 2013. https://arxiv.org/abs/1301.3781.

[2] T. Mikolov, K. Chen, G. Corrado, and J. Dean, “Distributed Representations of Words and Phrases and their Compositionality,” 2013. [Online]. Available: https://papers.nips.cc/paper/2013/file/9aa42b31882ec039965f3c4923ce901b-Paper.pdf.

[3] T. Mikolov, M. Karafiát, L. Burget, J. Honza, quot; Cernock´ycernock´y, and S. Khudanpur, “Recurrent neural network based language model,” 2010. [Online]. Available: https://www.isca-speech.org/archive/archive_papers/interspeech_2010/i10_1045.pdf.