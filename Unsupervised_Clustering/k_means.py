import random

def tsv_to_features(tsv_string):
    """Converts a tsv string into a map object of lists of features."""
    return list(map(lambda line: list(map(float, line.split('\t'))),
                            tsv_string.split('\n')))

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

def select_original_means(k, training_set):
    means = {}
    while k > 0:
        mu = training_set[random.randrange(len(training_set))]
        if not mu in means.values():
            k -= 1
            means[k] = mu
    return means

def generate_k_means(k, extremes):
    """Returns k means generated uniformly in the bounds of the extremes."""
    mus = {}
    count = 0
    for i in range(k):
        mu_i = []
        for extreme in extremes:
            mu_i.append(random.uniform(extreme[0], extreme[1]))
        mus[count] = mu_i
        count += 1
    return mus

def label_points(means, training_set, norm_calc):
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
                      lambda j: norm_calc(training_set[i], means[j])))
    return labels

def get_std_dev(means, labels, training_set, difference):
    std_devs = {}
    counts = {}
    for i in range(len(labels)):
        std_devs[labels[i]] = std_devs.get(labels[i], 0)
        std_devs[labels[i]] += difference(means[labels[i]], training_set[i])**2
        counts[labels[i]] = counts.get(labels[i], 0) + 1
    for key in std_devs:
        std_devs[key] /= counts[key] - 1
        std_devs[key] = (std_devs[key]) ** (1/2)
    return std_devs


def recalculate_means(labels, training_set, old_means):
    """Given the labels and the corresponding examples, returns new means."""
    means = {}
    nums = {}
    for c in range(len(labels)):
        means[labels[c]] = means.get(labels[c], {})
        for j in range(len(training_set[c])):
            means[labels[c]][j] = means[labels[c]].get(j,0) + training_set[c][j]
        nums[labels[c]] = nums.get(labels[c], 0) + 1
    for k in range(len(old_means)):
        means[k] = means.get(k, old_means[k])
    for k in range(len(means)):
        for j in range(len(means.get(k))):
            means[k][j] /= nums[k]
    return means

def k_means(k, training_set, norm_calc):
    """Given a k, a training set, and a vector difference function, cluster.

    This algorithm uses the k-means clustering algorithm to cluster a set of
    data into k means; it calculates the difference between two 
    data points using the norm_calc function provided by the user."""
    labels = []
    means = select_original_means(k, training_set)
    #means = generate_k_means(k, get_extreme_features(training_set))
    while True:
        labels = label_points(means, training_set, norm_calc)
        new_means = recalculate_means(labels, training_set, means)
        if means == new_means:
            break
        means = new_means
    std_devs = get_std_dev(means, labels, training_set, norm_calc)
    return (means, std_devs)
    #eturn [(means[i], std_devs[i]) for i in means]
