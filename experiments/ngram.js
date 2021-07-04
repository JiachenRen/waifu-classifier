const fs = require('fs');
const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// - Mark: Utils

/**
 * Returns a padding string of length n to append to the front of text as a pre-processing step to building n-grams
 * @param n length of word
 */
function startPad(n) {
    return [...'～'.repeat(n)];
}

/**
 * Creates n-gram tuples from text
 * @param n n-gram
 * @param text a string/sentence
 * @returns {[]} an array of sentence structured as grams
 */
function ngrams(n, text) {
    let words = startPad(n);
    words.push(...sentToWords(text));
    let grams = [];
    for (let i = n; i < words.length; i++) {
        grams.push([words.slice(i - n, i).join(' '), words[i]]);
    }
    return grams;
}

/**
 * Converts a sentence to a list of words
 *
 * Removes punctuations except '
 *
 * @param sent
 * @returns {string[]}
 */
function sentToWords(sent) {
    return sent.trim()
        .split(/\s/gi)
        .map(w => w.toLowerCase().replace(/(?!['])\W/gi, ''))
        .filter(w => w.length !== 0);
}

function addOne(counter, e) {
    if (e in counter) {
        counter[e] += 1;
    } else {
        counter[e] = 1;
    }
}

function getCount(counter, e) {
    if (e in counter) {
        return counter[e];
    }
    return 0;
}

function createNGramModel(trainPath, n = 2) {
    let model = new NgramModel(n);
    const lines = fs.readFileSync(trainPath, 'utf8').split('\n');
    lines.forEach(line => model.update(line));
    return model;
}

// - Mark: Model

class Probability {
    constructor(n, prob, prediction) {
        this.n = n;
        this.prob = prob;
        this.prediction = prediction;
    }

    toString() {
        return `'n = ${this.n}\t prob = ${this.prob}\t '${this.prediction}'`
    }

    compareTo(other) {
        // First compare n-gram, prioritize higher n
        if (this.n === other.n) {
            return this.prob - other.prob;
        }
        return this.n - other.n;
    }
}

class NgramModel {
    /**
     * Constructs an n-Gram back-off model.
     *
     * @param n up to n-gram.
     */
    constructor(n) {
        this.n = n;
        this.vocab = new Set();
        this.vocabSorted = null;
        this.contextCounter = {};
        this.occurrences = {};
    }

    /**
     * Updates (trains) the model with the text (sentence)
     * @param text a sentence
     */
    update(text) {
        let self = this;
        sentToWords(text).forEach(w => self.vocab.add(w));
        for (let i = 1; i < this.n + 1; i++) {
            let grams = ngrams(i, text);
            let self = this;
            grams.forEach(g => {
                addOne(self.occurrences, g);
                addOne(self.contextCounter, g[0]);
            });
        }
    }

    /**
     * Computes probability of word given context.
     *
     * @param context a string denoting the context, can contain multiple words
     * @param word a string
     * @returns {Probability} n-gram probability
     */
    prob(context, word) {
        let contextWords = sentToWords(context);
        // Take a maximum of n trailing words
        contextWords = contextWords.slice(Math.max(contextWords.length - this.n, 0));
        for (let i = 0; i < contextWords.length; i++) {
            let ctx = contextWords.slice(i);
            let ctxStr = ctx.join(' ');
            let occurrences = getCount(this.occurrences, [ctxStr, word]);
            let contextCount = getCount(this.contextCounter, ctxStr);
            if (occurrences !== 0 && contextCount !== 0)
                return new Probability(ctx.length, (occurrences) / (contextCount), word);
        }
        return new Probability(0, 0, word);
    }

    /**
     * Master prediction method. Generates a variable length prediction
     * of maximum of {maxWords} words, taking cues from n gram and probability information.
     *
     * @param maxWords max number of words in the generated prediction
     * @param context string of context words
     * @returns {Probability[]} predictions and their probabilities
     */
    predict(context, maxWords) {
        let predictions = [];
        for (let i = 1; i <= maxWords; i++) {
            predictions.push(...this.predictNextWords(context, i));
        }
        return predictions.sort((a, b) => b.compareTo(a));
    }

    /**
     * Predicts next n words given context via breadth first search.
     *
     * @param breadth is the search breadth
     * @param context string of context words
     * @param n number of predictions
     */
    predictNextWords(context, n, breadth = 5) {
        // Base case
        if (n === 1) {
            return this.predictNextWord(context)
                .slice(0, breadth)
                .filter(e => e.n >= n);
        }
        let predictions = this.predictNextWords(context, n - 1, breadth);
        let words = sentToWords(context);
        let aggregated = [];
        predictions.forEach((pred) => {
            let newContext = [...words, pred.prediction].join(' ');
            let newPredictions = this.predictNextWord(newContext).slice(0, breadth);
            newPredictions.forEach(e => {
                let phrase = pred.prediction + ' ' + e.prediction;
                let prob = pred.prob * e.prob;
                aggregated.push(new Probability(e.n, prob, phrase));
            });
        });
        return aggregated
            .sort((a, b) => b.compareTo(a))
            .slice(0, breadth)
            .filter(e => e.n >= n);
    }

    /**
     * Predicts the next word given the context.
     * @param context a string of context words
     * @return {Probability[]} array of Probabilities sorted first by n, then by prob.
     */
    predictNextWord(context) {
        let self = this;
        return Array.from(this.vocab)
            .map(w => self.prob(context, w))
            .filter(e => e.prob !== 0)
            .sort((a, b) => {
                return b.compareTo(a);
            });
    }

    /**
     * Sample a random word from the NGram language model.
     *
     * @param context words before the random word
     * @returns {string} a random word following given context
     */
    randomWord(context) {
        let r = Math.random();
        if (this.vocabSorted == null) {
            this.vocabSorted = Array.from(this.vocab);
            this.vocabSorted.sort();
        }
        let s = 0;
        for (const v of this.vocabSorted) {
            s += this.prob(context, v).prob;
            if (s > r) {
                return v;
            }
        }
    }

    /**
     * Generates a random paragraph of text of given length according to the NGram Model.
     *
     * @param length
     * @returns {string}
     */
    randomText(length) {
        let words = [Array.from(this.vocab)[Math.floor(Math.random() * this.vocab.size)]];
        while (words.length < length + this.n) {
            let nextWord = this.randomWord(words.slice(-this.n).join(' '));
            words.push(nextWord);
        }
        return words.join(' ');
    }
}

// - Mark: Driver code

// Creates an NGram model
let model = createNGramModel('../data/waifu_descriptions.txt', n = 3);

function repl() {
    rl.question('> length: ', (length) => {
        let text = model.randomText(length);
        console.info(text);
        console.info('\n');
        repl();
    });
}

repl();