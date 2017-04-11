import k_means as km
import numpy as np
import operator
import random
import sys

def difference(v1, v2, compare=False):
    """Difference using only the second feature."""
    if compare:
        return v1 - v2[0]
    else:
        return abs(v1[0] - v2[0])

def get_contents():
    filename = ""
    contents = ""
    k = 0
    trials = 0
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Test filename: ")
    if len(sys.argv) > 2:
        k = int(sys.argv[2])
    else:
        k = int(input("Input k: "))
    if len(sys.argv) > 3:
        trials = int(sys.argv[3])
    else:
        trials = int(input("Number of trials: "))
    with open(filename, 'r') as f:
        contents = f.read().rstrip()
    return k, trials, contents

def run_trial(k, contents):
    return km.k_means(k, km.tsv_to_features(contents), difference)

def run():
    random.seed()
    k, num_trials, contents = get_contents()
    k_results = {'mues': {}, 'sigmas': {}, 'acc': [], 'iters': []}
    for trial in range(num_trials):
        #print('Trial ' + str(trial + 1) + '/' + str(num_trials) + ' in progress.', end='\r')
        means, sigmas, iters, acc = run_trial(k,contents)
        mean_sigmas = sorted([(means[k][0], sigmas[k]) for k in means])
        k_results['iters'].append(iters)
        k_results['acc'].append(acc)
        for i in means:
            k_results['mues'][i] = k_results['mues'].get(i, [])
            k_results['mues'][i].append(mean_sigmas[i][0])
            k_results['sigmas'][i] = k_results['sigmas'].get(i,[])
            k_results['sigmas'][i].append(mean_sigmas[i][1])
    # Get the means
    k_results['mu_mu'] = {k: np.mean(list(k_results['mues'][k])) for k in k_results['mues']} 
    k_results['mu_sigma'] = {k: np.mean(list(k_results['sigmas'][k])) for k in k_results['sigmas']} 
    # Now get the std deviation of each
    k_results['sigma_mu'] = {k: np.std(list(k_results['mues'][k])) for k in k_results['mues']}
    k_results['sigma_sigma'] = {k: np.std(list(k_results['sigmas'][k])) for k in k_results['sigmas']}
    k_results['mu_iters'] = np.mean(k_results['iters'])
    k_results['sigma_iters'] = np.std(k_results['iters'])
    print('k-means results:')
    print('mu_acc')
    print(np.mean(k_results['acc']))
    print('mu_iters\tsigma_iters')
    print(str(k_results['mu_iters']) + '\t' + str(k_results['sigma_iters']))
    k_results = sorted([(k_results['mu_mu'][k], k_results['sigma_mu'][k], k_results['mu_sigma'][k], k_results['sigma_sigma'][k]) for k in k_results['mues']])
    #print('\x1b[2K\r', end ='') # Clears the progress line completely
    print('mu_mu\tsigma_mu\tmu_sigma\tsigma_sigma')
    for result in k_results:
        print('\t'.join(map(str,result)))

run()
