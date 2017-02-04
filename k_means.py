"""You should define a difference(v1,v2) function to calculate the differences between two feature vectors."""

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

def label_points(means, training_set):
    """Returns a list of labels corresponding to the training set."""
    def argmin(arguments, function):
        arg = 0
        minimum = function(arg)
        for i in range(1, len(arguments)):
            if function(arguments[i]) < minimum:
                minimum = function(arguments[i])
                arg = i
        return arg
    labels = []
    for i in range(len(training_set)):
        labels.append(argmin(list(range(len(means))),
                      lambda j: difference(training_set[i], means[j])))
    return labels

def recalculate_means(labels, training_set):
    """Given the labels and the corresponding examples, returns new means."""
    means = {}
    nums = {}
    for c in range(len(labels)):
        means[labels[c]] = means.get(labels[c], {})
        for j in range(len(training_set[c])):
            means[labels[c]][j] = means[labels[c]].get(j,0) + training_set[c][j]
        nums[labels[c]] = nums.get(labels[c], 0) + 1
    for k in range(len(means)):
        for j in range(len(means[k])):
            means[k][j] /= nums[k]
    return means

def k_means(k, training_set):
    labels = []
    means = generate_k_means(k, get_extreme_features(training_set))
    while True:
        labels = label_points(means, training_set)
        new_means = recalculate_means(labels, training_set)
        if means == new_means:
            break
        means = new_means
    return (means, labels)
