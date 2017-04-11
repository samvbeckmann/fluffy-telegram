#include<iostream>
#include<random>
#include<fstream>
#include<algorithm>
#include<ctime>
#include<vector>
#include<cstdlib>
#include<numeric>
#include "runner.hpp"

template <typename T> int sgn(T val) {
    return (T(0) < val) - (val < T(0));
}

int main(int argc, char* argv[]) {
    int trials = 0;
	srand(time(NULL));
	if (argc == 1) {
		std::cout << "Expected file!" << std::endl;
		return 1;
	}
    if (argc == 3) {
        trials = atoi(argv[2]);
    } else {
        trials = 1;
    }

    bool plural = trials != 1;
    std::cout<<"Running "<< trials << " trial" << (plural?"s.":".")<< std::endl;
	// Seed the random generator
	std::random_device rng;
    std::mt19937 urng(rand());

	// Load the training examples
    std::ifstream inputData;
    inputData.open(argv[1]);
    int m, f; // Where m is the number of examples, and f features per example
    inputData >> m >> f;
	std::cout << "Examples: " << m << "\tFeatures: " << f << std::endl;
    std::vector< std::vector <double> > initial(m,std::vector<double> (f+1,0));
    std::vector<double> data (f+1, 0);
    for (int i = 0; i < m; i++) {
        inputData >> data[0];
        for (int j = 1; j < f + 1; j++) {
            inputData >> data[j];
        }
        initial[i] = data;
    }

	std::cout << "Test size: " << m/5 << std::endl;
	std::cout << "Valid size: " << m/10 << std::endl;
	std::cout << "Train size: " << m - m/5 - m/10 << std::endl;

    std::vector<double> accuracy (trials, -100000000); // The accuracy vector
    for (int trial = 0; trial < trials; trial++) {
        std::cout << "Trial " << trial+1 << "/" << trials << "\r" << std::flush;
    	// Shuffle the labelled examples
        auto labelled(initial);
        std::shuffle(std::begin(labelled), std::end(labelled), urng);

    	// Move the labels to a different vector and partition the data
    	std::vector<std::vector <double> > testing(m/5, std::vector<double>(f, 0));
    	std::vector<std::vector <double> > valid(m/10, std::vector<double>(f, 0));
    	std::vector<std::vector <double> > train(m - m/10 - m/5, std::vector<double>(f, 0));

    	std::vector<int> yTesting(m/5, 0);
    	std::vector<int> yValid(m/10, 0);
    	std::vector<int> yTrain(m - m/10 - m/5, 0);

    	// 20% test, 10% validation, rest training
        for (int i = 0; i < m/5; i++) {
            yTesting[i] = labelled[i][0];
    		labelled[i].erase(labelled[i].begin());
    		testing[i] = labelled[i];
        }

        for (int i = m/5; i < m/5 + m/10; i++) {
    		int j = i - m/5;
            yValid[j] = labelled[i][0];
    		labelled[i].erase(labelled[i].begin());
    		valid[j] = labelled[i];
        }

    	for (int i = m/10 + m/5; i < m; i++) {
    		int j = i - m/10 - m/5;
    		yTrain[j] = labelled[i][0];
    		labelled[i].erase(labelled[i].begin());
    		train[j] = labelled[i];
    	}

    	// Perform training & testing (note that currently the valid set is unused)
    	double tests = 0;
    	double correct = 0;
    	SMO::kernel chosenKernel = SMO::gaussianKernel;//SMO::polyKernel(0, 1);
    	auto results = SMO::train(1E10, 1E-7, 10, train, yTrain, chosenKernel);
    	for (int i = 0; i < testing.size(); i++) {
    		double guess = SMO::predict(testing[i], results.first, results.second, chosenKernel);
    		int value = sgn(guess);
    		if (value == 0) {
    			value = 1;
    		}
    		tests++;
    		if (value == yTesting[i]) { // Correct
    			correct++;
    		}
    	}
        accuracy[trial] = 100*correct/tests;
    	//std::cout << "Accuracy on trial " << trial << ": " << accuracy[trial] << "%" << std::endl;
    }

    std::cout << "Ran " << trials << " trials!" << std::endl;

    // Calculate final statistics
    double mean = std::accumulate(accuracy.begin(), accuracy.end(), 0.0)/trials;
    double sq_sum = std::inner_product(accuracy.begin(), accuracy.end(), accuracy.begin(), 0.0);
    double std_dev = std::sqrt(sq_sum/trials - mean*mean);

    // Output results
    std::cout << std::endl << "Results:" << std::endl;
    std::cout << "Accuracy mean: " << mean << "%" << std::endl;
    std::cout << "Accuracy std dev: " << std_dev << "%" << std::endl;

    return 0;
}
