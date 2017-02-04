"""You should define a difference(v1,v2) function to calculate the differences between two feature vectors."""

import sys
import random

def tsv_to_features(tsv_string):
    """Converts a tsv string into a map object of lists of features."""
    return map(lambda line: list(map(float, line.split('\t'))),
                            tsv_string.split('\n'))

def get_extreme_features(training_set):
    """Returns a list of tuples: (min_i, max_i) for each feature i."""
    extremes = []
    for features in training_set:
        for i in range(len(features)):
            if len(extremes) < len(features):
                extremes.append((features[i], features[i]))
            else:
                extremes[i] = (min(extremes[i][0], features[i]),
                               max(extremes[i][1], features[i]))
    return extremes

def generate_k_means(k, extremes):
    """Returns k means generated uniformly in the bounds of the extremes."""
    mus = []
    for i in range(k):
        mu_i = []
        for j in range(len(extremes)):
            mu_i.append(random.uniform(extremes[j][0], extremes[j][1]))
        mus.append(mu_i)
    return mus

