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

def parse_trials(string):
    regex = '(\.\..+?)\nk-means.+?mu_mu.+?\n(.+?)(?=\.\.)'
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
    clusters = trial_tuple[1]
    
    results[name] = results.get(name, {'iters': [], 'means': {}, 'covs': {}})
    clusters = dissect(clusters)
    cluster_proper = list(map(list, zip(*clusters)))
    print(r'$\mu_{\mu_{' + str(count) + '}}$', end='')
    for item in cluster_proper[0]:
        print_helper(item)
    print(r'\\')
    print(r'$\sigma_{\mu_{' + str(count) + '}}$', end='')
    for item in cluster_proper[1]:
        print_helper(item)
    print(r'\\')
    print(r'$\mu_{\sigma_{' + str(count) + '}}$', end='')
    for item in cluster_proper[2]:
        print_helper(item)
    print(r'\\')
    print(r'$\sigma_{\sigma_{' + str(count) + '}}$', end='')
    for item in cluster_proper[3]:
        print_helper(item)
    print(r'\\\midrule')
    
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


