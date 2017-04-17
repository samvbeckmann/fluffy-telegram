import math
import random

class Bayes_Classifier:
    '''A naive bayes classifier

    Given a list of labeled documents (tuples of label, words), constructs
    a classifier that can subsequently classify arbitrary text'''
    def add_document(self, document):
        'Adds the document to the vocabulary of this classifier'
        label = document[0]
        self.unique_labels.add(label)
        text = document[1]
        vocabulary = self.vocabulary
        vocabulary[label] = vocabulary.get(label, {})
        words = text.split()
        if self.ignore_case:
            words = [word.lower() for word in words]
        for word in words:
            self.word_counts[label] = self.word_counts.get(label, 0) + 1
            vocabulary[label][word] = vocabulary[label].get(word, 0) + 1

    def __init__(self, documents=[], ignore_case=True):
        'Initializes with the documents and whether to ignore case'
        self.vocabulary = {} # Maps labels to maps of words to frequencies
        self.unique_labels = set() # The set of all of the labels
        self.word_counts = {} # Total counts of words for each label
        self.ignore_case = ignore_case

        for document in documents:
            self.add_document(document)

    def classify(self, text, getprobs=False):
        'Classifies the text provided based on the current vocabulary'
        vocabulary = self.vocabulary
        likelihoods = {}
        for label in self.unique_labels:
            likelihoods[label] = 0
        words = text.split()
        if self.ignore_case:
            words = [word.lower() for word in words]
        for word in words:
            for label in self.unique_labels:
                if word in vocabulary[label]:
                    likelihoods[label] += math.log(vocabulary[label][word]/
                                                   self.word_counts[label])
                else:
                    likelihoods[label] += math.log(1.0/self.word_counts[label])
        if getprobs:
            # normalize
            probs = {k: math.exp(v) for (k, v) in likelihoods.items()}
            return {k: v/sum(probs.values()) for (k,v) in probs.items()}
        else:
            return list(filter(lambda x: likelihoods[x] ==
                max(likelihoods.values()), likelihoods))

