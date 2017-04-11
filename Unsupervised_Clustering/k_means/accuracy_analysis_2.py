''' This parser scans the output of EM for data

This parser obtains information about EM, particularly:
1. The number of convergences for each trial, by file
2. The results of each trial, by file

It converts this information, then, into
1. The means & std deviations of the number of convergences
2. The means & std deviations of the means of each file
3. The means & std deviations of the covariances of each file
'''
import re
import numpy as np

results = {}
count = 0

def get_closest_mean(point, orig_means):
    index = 0
    point = float(point)
    means = list(map(float, orig_means))
    distance = abs(point - means[0])
    for i in range(1, len(means)):
        if abs(point - means[i]) < distance:
            distance = abs(point - means[i])
            index = i
    return orig_means[index]

def get_actual_labels(filename):
    contents = ''
    with open(filename) as f:
        contents = f.read()
    labels = {}
    lines = contents.rstrip().split('\n')
    means = [x[0] for x in [line.split('\t') for line in lines]]
    values = [x[1] for x in [line.split('\t') for line in lines]]
    for i in range(len(means)):
        labels[values[i]] = means[i]
    return labels

def get_test_labels(filename, identified_means):
    contents = ''
    with open(filename) as f:
        contents = f.read()
    labels = {}
    lines = contents.rstrip().split('\n')
    values = [x[1] for x in [line.split('\t') for line in lines]]
    for value in values:
        mean = get_closest_mean(value, identified_means)
        labels[mean] = labels.get(mean, [])
        labels[mean].append(value)
    return labels

def parse_trials(string):
    regex = '(\.\..+?) .+?\nk-means.+?mu_mu.+?\n(.+?)(?=\.\.)'
    regex = re.compile(regex, re.M | re.S)
    return regex.findall(string)

def dissect(clusters):
    regex = '(.+?)\t(.+?)\t(.+?)\t(.+?)\n'
    regex = re.compile(regex, re.M | re.S)
    return regex.findall(clusters)

def parse_trial(trial_tuple):
    def print_helper(stat):
        print(' & {0:.3f}'.format(float(stat)), end='')
    global count
    count += 1
    name = trial_tuple[0]
    actual_labels = get_actual_labels(name)
    clusters = trial_tuple[1]
    test_means = list(map(lambda x: x[0], sorted(dissect(clusters))))
    test_labels = get_test_labels(name, test_means)
    correct = 0
    for mean in test_labels:
        for j in range(len(test_labels[mean])):
            for i in range(j, len(test_labels[mean])):
                if actual_labels[test_labels[mean][j]] == actual_labels[test_labels[mean][i]]:
                    correct += 1
    total = len(actual_labels)*(len(actual_labels) - 1)/2
    print(name + '\t' + str(correct/total))

    # results[name] = results.get(name, {'iters': [], 'means': {}, 'covs': {}})
    # cluster_proper = list(map(list, zip(*clusters)))
    # print(r'$\mu_{\mu_{' + str(count) + '}}$', end='')
    # for item in cluster_proper[0]:
    #     print_helper(item)
    # print(r'\\')
    # print(r'$\sigma_{\mu_{' + str(count) + '}}$', end='')
    # for item in cluster_proper[1]:
    #     print_helper(item)
    # print(r'\\')
    # print(r'$\mu_{\sigma_{' + str(count) + '}}$', end='')
    # for item in cluster_proper[2]:
    #     print_helper(item)
    # print(r'\\')
    # print(r'$\sigma_{\sigma_{' + str(count) + '}}$', end='')
    # for item in cluster_proper[3]:
    #     print_helper(item)
    # print(r'\\\midrule')
    
def get_statistics():
    stats = {}
    for case in results:
        data = results[case]
        stats[case] = {}
        stats[case]['mean_mus'] = {x: np.mean(data['means'][x]) for x in range(len(data['means']))}
        stats[case]['cov_mus'] = {x: np.mean(data['covs'][x]) for x in range(len(data['covs']))}
        stats[case]['mean_devs'] = {x: np.std(data['means'][x]) for x in range(len(data['means']))}
        stats[case]['cov_devs'] = {x: np.std(data['covs'][x]) for x in range(len(data['covs']))}
    return stats

def display_stats(stats):
    def print_helper(stat):
        print(' & {0:.4f}'.format(stat), end='')
    count = 1
    for case in stats:
        data = stats[case]
        print(r'$\mu_{\mu_{' + str(count) + '}}$', end='')
        for i in range(len(data['mean_mus'])):
            print_helper(data['mean_mus'][i])
        print(r'\\')
        print(r'$\sigma_{\mu_{' + str(count) + '}}$', end='')
        for i in range(len(data['mean_mus'])):
            print_helper(data['mean_devs'][i])
        print(r'\\')
        print(r'$\mu_{\sigma_{' + str(count) + '}}$', end='')
        for i in range(len(data['mean_mus'])):
            print_helper(data['cov_mus'][i])
        print(r'\\')
        print(r'$\sigma_{\sigma_{' + str(count) + '}}$', end='')
        for i in range(len(data['cov_devs'])):
            print_helper(data['cov_devs'][i])
        print(r'\\\midrule')
        count += 1


with open('output.txt') as f:
    trials = parse_trials(f.read())
    for trial in trials:
        parse_trial(trial)
    #display_stats(get_statistics())


