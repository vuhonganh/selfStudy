function H = calHessian(theta, Y, X)

% get number of data
[m, n] = size(X);

% init H
H = zeros(n , n);

for i = 1:m
    zi = Y(i) * X(i, :) * theta;
    term = 1/m * Y(i) * Y(i) * mySigmoid(zi) * (1 - mySigmoid(zi));
    H = H + term * X(i,:)' * X(i,:);
end
