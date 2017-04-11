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

def parse_trials(string):
    regex = '\d+ (.+?)\nEM.+?N.+?\: (\d+)\n(.+?)\n\n(?=\d)'
    regex = re.compile(regex, re.M | re.S)
    return regex.findall(string)

def dissect(clusters):
    regex = 'Mean \d\:.+?([-+]?\d*\.\d+|\d+).+?Cov \d\:.+?([-+]?\d*\.\d+|\d+).+?'
    regex = re.compile(regex, re.M | re.S)
    return regex.findall(clusters)

def parse_trial(trial_tuple):
    name = trial_tuple[0]
    iters = int(trial_tuple[1])
    clusters = trial_tuple[2]
    
    results[name] = results.get(name, {'iters': [], 'means': {}, 'covs': {}})
    results[name]['iters'].append(iters)
    clusters = [(float(a), float(b)) for a, b in dissect(clusters)]
    means, covs = zip(*sorted(clusters))
    for x in range(len(means)):
        results[name]['means'][x] = results[name]['means'].get(x, [])
        results[name]['means'][x].append(means[x])
        results[name]['covs'][x] = results[name]['covs'].get(x, [])
        results[name]['covs'][x].append(covs[x])
    
def get_statistics():
    stats = {}
    for case in results:
        data = results[case]
        stats[case] = {}
        stats[case]['iter_mus'] = np.mean(data['iters'])
        stats[case]['iter_devs'] = np.std(data['iters'])
        stats[case]['mean_mus'] = {x: np.mean(data['means'][x]) for x in range(len(data['means']))}
        stats[case]['cov_mus'] = {x: np.mean(data['covs'][x]) for x in range(len(data['covs']))}
        stats[case]['mean_devs'] = {x: np.std(data['means'][x]) for x in range(len(data['means']))}
        stats[case]['cov_devs'] = {x: np.std(data['covs'][x]) for x in range(len(data['covs']))}
    return stats

def display_stats(stats):
    for case in stats:
        data = stats[case]
        print('Case: ' + case)
        print('  Iters Mu: ' + str(data['iter_mus']))
        print('  Iters Std: ' + str(data['iter_devs']))
        print('  Mean Mus: ' + str(data['mean_mus']))
        print('  Mean Std: ' + str(data['mean_devs']))
        print('  Cov Mus: ' + str(data['cov_mus']))
        print('  Cov Std: ' + str(data['cov_devs']))
        print()


with open('results.txt') as f:
    trials = parse_trials(f.read())
    for trial in trials:
        parse_trial(trial)
    display_stats(get_statistics())


