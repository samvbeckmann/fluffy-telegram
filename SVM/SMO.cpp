#include<iostream>
#include<fstream>
#include<utility>
#include<cmath>
#include<cstdlib>
#include<time.h>
#include<algorithm>
#include<vector>

namespace SMO {

// Given two vectors, returns a calculation based on them.
// The simplest case is the dot product.
typedef std::function<double(std::vector<double>, std::vector<double>)> kernel;
struct SupportVector {
	std::vector<double> example;
	int label;
	double alpha;
};

int get_rand_without(int max, int without) {
	int choice;
	do {
		choice = rand() % max;
	} while (choice == without);

	return choice;
}

double predict(std::vector<double> x, std::vector<SupportVector> supports,
		       double b, kernel k) {
	double result = 0;
	for (int i = 0; i < supports.size(); i++) {
		result += supports[i].alpha*supports[i].label*k(supports[i].example, x);
	}
	return result + b;
}

} // End namespace

// For use when training the SMO algorithm
double predict_internal(std::vector<double> alpha, std::vector<double> x,
		std::vector< std::vector<double> > examples, std::vector<int> y,
		double b, SMO::kernel k) {
	double result = 0;
	for (int i = 0; i < examples.size(); i++) {
		result += alpha[i]*y[i]*k(examples[i], x);
	}
	return result + b;
}

namespace SMO {
/* The simplified SMO algorithm.
 * C: Regularization parameter
 * tol: Numerical tolerance
 * max_passes: Number of passes permitted
 * x: A vector of example vectors
 * y: A vector of labels corresponding to the examples in x
 * k: The kernel to use
 */
std::pair<std::vector<SupportVector>, double> train(double C, double tol, int max_passes,
		std::vector< std::vector<double> >x, std::vector<int> y, kernel k) {
	int m = x.size();
	double b = 0;
	std::vector<double> alpha (m);
	int passes = 0;
	std::vector<double> E (m);
	int count = 0;

	// This while loop can be converted to a for loop and num_changed eliminated
	while (passes < max_passes) {
		int num_changed = 0;
		for (int i = 0; i < m; i++) {
			E[i] = predict_internal(alpha, x[i], x, y, b, k) - y[i];
			if ((y[i]*E[i] < -tol && alpha[i] < C)
				|| (y[i]*E[i] > tol && alpha[i] > 0)) {
				int j = get_rand_without(m, i);
				E[j] = predict_internal(alpha, x[j], x, y, b, k) - y[j];
				double L, H;
				if (y[i] != y[j]) {
						L = std::max(0., alpha[j] - alpha[i]);
						H = std::min(C, C + alpha[j] - alpha[i]);
				} else {
						L = std::max(0., alpha[i] + alpha[j] - C);
						H = std::min(C, alpha[i] + alpha[j]);
				}
				if (L == H) {
					continue;
				}
				double eta = 2*k(x[i], x[j]) - k(x[i], x[i]) - k(x[j], x[j]);
				if (eta >= 0) {
					continue;
				}
				double alpha_i_old = alpha[i];
				double alpha_j_old = alpha[j];
				alpha[j] -= y[j]*(E[i] - E[j])/eta;
				alpha[j] = std::max(std::min(alpha[j], H), L);
				if (std::abs(alpha[j] - alpha_j_old) < tol) {
					continue;
				}
				alpha[i] += y[i]*y[j]*(alpha_j_old - alpha[j]);
				double b1 = b - E[i] - y[i]*(alpha[i] - alpha_i_old)*k(x[i],
						    x[i]) - y[j]*(alpha[j] - alpha_j_old)*k(x[i], x[j]);
				double b2 = b - E[j] - y[i]*(alpha[i] - alpha_i_old)*k(x[i],
						    x[j]) - y[j]*(alpha[j] - alpha_j_old)*k(x[j], x[j]);

				if (0 < alpha[i] && alpha[i] < C) {
					b = b1;
				} else if (0 < alpha[j] && alpha[j] < C) {
					b = b2;
				} else {
					b = (b1 + b2)/2.0;
				}

				num_changed++;
			}
		}
		std::cout << "Iterations: " << ++count << "\r" << std::flush;
		if (num_changed == 0) {
				passes++;
		} else {
				passes = 0;
		}
	}
	std::cout << std::endl;

	std::vector<SupportVector> supports;
	for (int i = 0; i < m; i++) {
		if (alpha[i] != 0) {
			SupportVector support;

			support.example = x[i];
			support.label = y[i];
			support.alpha = alpha[i];

			supports.push_back(support);
		}
	}
	return std::make_pair(supports, b);
}

// The simple kernel: The dot product
double dot(std::vector<double> x1, std::vector<double> x2) {
	double result = 0;
	for (int i = 0; i < x1.size(); i++) {
		result += x1[i]*x2[i];
	}
	return result;
}

// A function that generates a polynomial kernel from the input parameters
// std::function<double (std::vector<double>, std::vector<double>)>
kernel polyKernel(double increase, double power) {
	return [increase, power](std::vector<double> x1, std::vector<double>x2 ) {
		return pow(dot(x1, x2) + increase, power);
	};
}

// The Gaussian/RBF kernel
double gaussianKernel(std::vector<double> x1, std::vector<double> x2) {
	double result = 0;
	for (int i = 0; i < x1.size(); i++) {
		result += pow(x1[i] - x2[i], 2);
	}
	result *= -1.0/(2);
	return exp(result);
}

} // End namespace
