import numpy as np
import math
import bayes_constructor as bc

mallory = ''
shakespeare = ''

num_trials = 1000

with open('../../Datasets/LeMorteDArthur.txt') as m:
    mallory = m.read()

with open('../../Datasets/Shakespeare.txt') as s:
    shakespeare = s.read()

mallory_words = mallory.split()
shakespeare_words = shakespeare.split()

m_test_size = 10
s_test_size = 10

print('Train sizes')
print(len(mallory_words) - m_test_size)
print(len(shakespeare_words) - s_test_size)

print('Test sizes')
print(m_test_size)
print(s_test_size)

m_correct = []
s_correct = []

for i in range(num_trials):
    print('Iteration ' + str(i+1) + '/' + str(num_trials), end='\r')
    m_words = list(mallory_words) # Protective copies
    s_words = list(shakespeare_words)

    # Shuffle to split into train and test
    np.random.shuffle(m_words)
    np.random.shuffle(s_words)

    m_test, m_train = ' '.join(m_words[:m_test_size]), ' '.join(m_words[m_test_size:])
    s_test, s_train = ' '.join(s_words[:s_test_size]), ' '.join(s_words[s_test_size:])

    classifier = bc.Bayes_Classifier([('M', m_train), ('S', s_train)])

    m_correct.append(1 if 'M' in classifier.classify(m_test) else 0)
    s_correct.append(1 if 'S' in classifier.classify(s_test) else 0)

print('Results summary (mean\tstd_dev):')
print(str(np.mean(m_correct)) + '\t' + str(np.std(m_correct)))
print(str(np.mean(s_correct)) + '\t' + str(np.std(s_correct)))
        
