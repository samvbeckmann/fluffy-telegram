function [avgMeans, avgCovariances] = run_tests(k, X, trials)
  avgMeans = cell(0);
  avgCovariances = cell(0);
  for j = 1:k
    avgMeans{j} = zeros(1, size(X, 2));
    avgCovariances{j} = zeros(size(X, 2), size(X, 2));
  endfor
  for t = 1:trials
    [resultM, resultC] = EM(k, X);
    for j = 1:k
      avgMeans{j} += resultM{j}/trials;
      avgCovariances{j} += resultC{j}/trials;
    endfor
  endfor
endfunction
