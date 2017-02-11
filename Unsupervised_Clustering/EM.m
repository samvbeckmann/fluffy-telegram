function [means, covariances] = EM(k, X)
  % The EM algorithm takes in k (for k Gaussian mixtures) and X, a matrix
  % wherein each row is a training example
  % len(X) >= k >= 1
  means = cell(k, 1);
  phis = cell(k, 1);
  covariances = cell(k, 1);
  weights = cell(k, 1);

  num_examples = size(X, 1);
  num_features = size(X, 2);
  choices = X(randperm(num_examples, k), :);

  % Initialization
  for j = 1:k
    weights{j} = rand(num_examples, 1);
  endfor

  old_means = cell(k, 1);

  % Begin EM algorithm
  do
    old_means = means;

    % M-step
    for j = 1:k
      phis{j} = mean(weights{j});
      means{j} = weights{j}'*X/sum(weights{j});
      differences = X - repmat(means{j}, num_examples, 1);
      covariances{j} =differences'*diag(weights{j})*differences/sum(weights{j});
    endfor

    normalizing_constant = mvnpdf(X, means{1}, covariances{1})*phis{j};
    for j = 2:k 
      normalizing_constant += mvnpdf(X, means{j}, covariances{j})*phis{j};
    endfor

    % E-step
    for j = 1:k 
      weights{j} = mvnpdf(X, means{j}, covariances{j})*phis{j}./normalizing_constant;
    endfor
  until (isequal(old_means,means))
endfunction
