#ifndef RUNNER_H
#define RUNNER_H
#include<vector>
#include<utility>

//// SMO Utilities
namespace SMO {
// Kernel
typedef std::function<double(std::vector<double>, std::vector<double>)> kernel; 
double dot(std::vector<double> x1, std::vector<double> x2);
kernel polyKernel(double increase, double power);
double gaussianKernel(std::vector<double> x1, std::vector<double> x2);

// SMO algorithm
struct SupportVector {                                                          
    std::vector<double> example;                                                
    int label;                                                                  
    double alpha;                                                               
};                                                                              


std::pair<std::vector<SupportVector>, double> train(double C, double tol, int max_passes,
        std::vector< std::vector<double> >x, std::vector<int> y, kernel k);

double predict(std::vector<double> x, std::vector<SupportVector> supports, 
        double b, kernel k);
}


#endif // RUNNER_H
