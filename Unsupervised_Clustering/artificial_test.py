import k_means as km
import operator
import sys

def difference(v1, v2, compare=False):
    """Difference using only the second feature."""
    if compare:
        return v1[1] - v2[1]
    else:
        return abs(v1[1] - v2[1])

def get_contents():
    filename = ""
    contents = ""
    k = 0
    trials = 0
    if len(sys.argv) > 1:
        k = int(sys.argv[1])
    else:
        k = int(input("Input k: "))
    if len(sys.argv) > 2:
        filename = sys.argv[2]
    else:
        filename = input("Test filename: ")
    if len(sys.argv) > 3:
        trials = int(sys.argv[3])
    else:
        trials = int(input("Number of trials: "))
    with open(filename, 'r') as f:
        contents = f.read().rstrip()
    return k, trials, contents

def run_trial(k, contents):
    means, sigmas = km.k_means(k, km.tsv_to_features(contents), difference)
    return means, sigmas

def run():
    k, num_trials, contents = get_contents()
    k_results = {'means': {}, 'std_devs': {}}
    for trial in range(num_trials):
        print('Trial ' + str(trial + 1) + '/' + str(num_trials) + ' in progress.', end='\r')
        means, sigmas = run_trial(k,contents)
        mean_sigmas = sorted([(means[k][1], sigmas[k]) for k in means])
        for i in means:
            k_results['means'][i] = k_results['means'].get(i, 0) + mean_sigmas[i][0]
            k_results['std_devs'][i] = k_results['std_devs'].get(i,0)+ mean_sigmas[i][1]
    k_results['means'] = {k: v/num_trials for (k, v) in k_results['means'].items()}
    k_results['std_devs'] = {k: v/num_trials for k, v in k_results['std_devs'].items()}
    k_results = sorted([(k_results['means'][k], k_results['std_devs'][k]) for k in k_results['means']])
    print('\x1b[2K\r', end ='') # Clears the progress line completely
    print('k-means results:')
    print('mean\tstd-dev')
    for result in k_results:
        print(str(result[0]) + '\t' + str(result[1]))

run()
