#include<armadillo>
#include<fstream>
#include<iostream>
#include<vector>
#include<math.h>

const static double TAU = 2*M_PI;

void deepCopy(arma::rowvec* src, int size, arma::rowvec* dst) {
	for (int i = 0; i < size; i++) {
		dst[i] = arma::rowvec(src[i]);
	}
}

bool equal(arma::rowvec* a, arma::rowvec* b, int size, double tol) {
	double diff = 0;
	for (int i = 0; i < size; i++) {
		diff += arma::sum(arma::abs(a[i] - b[i]));
		if (diff > tol) {
			return false;
		}
	}
	return true;
}

void normalize_weights(arma::colvec* weights, int size) {
	for (int i = 0; i < weights[0].n_rows; i++) {
		double sum_total = 0;
		for (int j = 0; j < size; j++) {
			sum_total += weights[j][i];
		}
		for (int j = 0; j < size; j++) {
			weights[j][i] /= sum_total;
		}
	}
}

inline void mvnpdf(arma::mat obs, arma::rowvec mean,
		           arma::mat cov, arma::colvec *out) {
	arma::mat R = arma::chol(cov);
	double denom = arma::prod(R.diag());
	if (denom < 1E-10) {
		denom = 1E-10;
	}
	double scale = pow(TAU, -((double) obs.n_cols)/2.0)/denom;
	*out=scale*arma::exp(-sum(arma::square((obs.each_row() - mean)*(R.i())), 1)/2.0);
}

inline int* getIntsWithoutReplacement(int max, int num) {
	int* indices = new int[num];
	for (int i = 0; i < num; i++) {
		int choice = rand() % max;
		for (int j = 0; j < i; j++) {
			if (choice == indices[j]) { // Duplicate
				choice = -1;
				break;
			}
		}
		if (choice != -1) {
			indices[i] = choice;
		} else {
			i--;
		}
	}
	return indices;
}

void makeMinimal(arma::mat* cov) {
	for (int i = 0; i < (int) cov -> n_elem; i++) {
		if ((*cov)[i] < 1E-10) {
			(*cov)[i] = 1E-10;
		}
	}
}

std::tuple<arma::rowvec*, arma::mat*, int> EM(int k, arma::mat X) {
	int count = 0;
	arma::rowvec* means = new arma::rowvec[k];
	arma::rowvec* old_means = new arma::rowvec[k];
    double* phis = new double[k];
	arma::mat* covs = new arma::mat[k];
	arma::mat differences;
	arma::colvec* weights = new arma::colvec[k];
	int* indices = getIntsWithoutReplacement(X.n_rows, k);

	// Randomize the weights
	for (int i = 0; i < k; i++) {
		weights[i] = arma::randu<arma::colvec>(X.n_rows);
	}
	normalize_weights(weights, k);
	for (int i = 0; i < k; i++) {
		means[i] = arma::rowvec(X.row(indices[i]));
		phis[i] = arma::sum(weights[i])/X.n_rows;
		covs[i] = arma::cov(X);
	}

	std::cout << "EM initialized—Running.\r" << std::flush;
	// Begin EM algorithm
	do {
		deepCopy(means, k, old_means);

		// E-step
		for (int j = 0; j < k; j++) {
			mvnpdf(X, means[j], covs[j], &weights[j]);
			weights[j]*=phis[j];
		}

		normalize_weights(weights, k);

		// M-step
		for (int j = 0; j < k; j++) {
			double sum = arma::sum(weights[j]);
			phis[j] = sum/weights[j].n_rows;
			means[j] = weights[j].t()*X/sum;
			// std::cout << means[j];
			differences = X.each_row() - means[j];
			covs[j] = differences.t()*arma::diagmat(weights[j])*differences/sum;
			makeMinimal(&covs[j]);
		}

		//std::cout << covs[0];

		count++;
		if (count % 10000 == 0) {
			std::cout << "Iteration " << count << " complete.\r" << std::flush;
		}

	} while (!equal(means, old_means, k, 1E-8));

	// delete old_means;
	// delete phis;
	// delete weights;

	return std::make_tuple(means, covs, count);
}

double get_accuracy(int k, std::tuple<arma::rowvec*, arma::mat*, int> tuple, arma::mat obs) {
	arma::colvec results = arma::zeros<arma::colvec>(obs.n_rows);
    for (int j = 0; j < k; j++) {
		arma::colvec temp = arma::zeros<arma::colvec>(obs.n_rows);
		mvnpdf(obs, std::get<0>(tuple)[j], std::get<1>(tuple)[j], &temp);
		for (int i = 0; i < obs.n_rows; i++) {
			// results[i] += temp[i];
			results[i] = temp[i] > results[i] ? temp[i] : results[i];
		}
	}
	return arma::sum(results)/results.n_rows;
}

int main(int argc, char* argv[]) {
	// Initialization
	srand(time(NULL));
	arma::arma_rng::set_seed(rand());

	// Load the data
	std::ifstream inputData;
	inputData.open(argv[1]);
	int m = atoi(argv[2]); // # examples
	int f = atoi(argv[3]); // # features
	int k = atoi(argv[4]); // # clusters
	int numSkip = argc == 6 ? atoi(argv[5]) : 0;
	f -= numSkip;
	arma::mat obs = arma::mat(m, f);
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < numSkip; j++) {
			inputData >> obs.at(i, 0);
		}
		for (int j = 0; j < f; j++) {
			inputData >> obs.at(i, j);
		}
	}

	auto item = EM(k, obs);
	std::cout << "Number of iterations: " << std::get<2>(item) << std::endl;
	std::cout << "Accuracy: " << get_accuracy(k, item, obs) << std::endl;
	for (int j = 0; j < k; j++) {
		std::cout << "Mean " << j << ": " << std::endl <<
			std::get<0>(item)[j] << "Cov " << j << ": " << std::endl <<
			std::get<1>(item)[j] << std::endl;
	}
}
