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

def reduce_means(means, mean_nums, num):
    '''Reduces the means provided to num; means must be sorted'''
    #means = list(means)
    #mean_nums = dict(mean_nums)
    def get_small_index(means):
        index = 0
        min_count = mean_nums[means[0]] + mean_nums[means[1]]
        count0 = mean_nums[means[0]]
        count1 = 0
        for i in range(1, len(means)):
            count1 = mean_nums[means[i]]
            if count0 + count1 < min_count:
                min_count = count0 + count1
                index = i - 1
            count0 = count1
            count1 = 0
        return index
    if num >= len(means):
        return means, mean_nums
    else:
        merge_index = get_small_index(means)
        mean0 = means.pop(merge_index)
        number0 = float(mean_nums.pop(mean0))
        mean1 = means[merge_index]
        number1 = float(mean_nums.pop(mean1))
        total = number0 + number1

        new_mean = float(mean0)*number0/total + float(mean1)*number1/total
        means[merge_index] = new_mean
        mean_nums[new_mean] = number0 + number1
        return reduce_means(means, mean_nums, num)

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

def get_actual_nums(filename):
    contents = ''
    with open(filename) as f:
        contents = f.read()
    mean_nums = {}
    lines = contents.rstrip().split('\n')
    means = [x[0] for x in [line.split('\t') for line in lines]]
    for value in means:
        mean_nums[value] = mean_nums.get(value, 0) + 1
    return mean_nums

def get_test_nums(filename, identified_means):
    contents = ''
    with open(filename) as f:
        contents = f.read()
    mean_test_nums = {}
    lines = contents.rstrip().split('\n')
    values = [x[1] for x in [line.split('\t') for line in lines]]
    for value in values:
        mean = get_closest_mean(value, identified_means)
        mean_test_nums[mean] = mean_test_nums.get(mean, 0) + 1
    return mean_test_nums
        
def parse_trials(string):
    regex = '(\.\..+?) .+?\nk-means.+?mu_mu.+?\n(.+?)(?=\.\.)'
    regex = re.compile(regex, re.M | re.S)
    return regex.findall(string)

def dissect(clusters):
    regex = '(.+?)\t(.+?)\t(.+?)\t(.+?)\n'
    regex = re.compile(regex, re.M | re.S)
    return regex.findall(clusters)

def percent_error(actual, approximate):
    return abs((float(actual) - float(approximate))/float(actual))

def get_error(actual_mean_dict, test_means):
    '''Actual_mean_dict must be a dictionary mapping means to frequency

    The keys must be the same size for actual_mean_dict and the list of
    test means'''
    total_num = sum(actual_mean_dict.values())
    error = 0
    test_means = sorted(map(float,test_means))
    keys = sorted(actual_mean_dict.keys(), key=float)
    for i in range(len(test_means)):
        local_error = percent_error(keys[i], test_means[i])
        error += actual_mean_dict[keys[i]]/total_num * local_error
    return error


def parse_trial(trial_tuple):
    def print_helper(stat):
        print(' & {0:.3f}'.format(float(stat)), end='')
    global count
    count += 1
    name = trial_tuple[0]
    mean_nums = get_actual_nums(name)
    clusters = trial_tuple[1]
    test_means = sorted([cluster[0] for cluster in dissect(clusters)])
    test_nums = get_test_nums(name, test_means)
    actual_means = sorted(mean_nums.keys())
    if len(mean_nums) > len(test_means):
        actual_means, mean_nums = reduce_means(actual_means, mean_nums, len(test_means))
    else:
        test_means, test_nums = reduce_means(test_means, test_nums, len(mean_nums))
    print(name)
    print(1 - get_error(mean_nums, test_means))
    print()

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


