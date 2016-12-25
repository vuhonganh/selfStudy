Xdata = load('logistic_x.txt');
Ydata = load('logistic_y.txt');

% number of data
m = size(Xdata, 1);

% add 1 into each data of X
X = [ones(m, 1), Xdata];
theta = zeros(size(X, 2), 1);
Y = Ydata;

nbIter = 100;

for i = 1:nbIter
    H = calHessian(theta, Y, X);
    grad = gradiantJ(theta, Y, X);
    theta = theta - H^(-1) * grad;
end

idxPos = find(Y == 1);
idxNeg = find(Y ~= 1);
figure; hold on;
% scatter data points
scatter(X(idxPos, 2), X(idxPos, 3), 'filled', 'red');
scatter(X(idxNeg, 2), X(idxNeg, 3), 'filled', 'blue');

% plot boundary by theta
x1 = min(X(:, 2)):0.01:max(X(:,2));
x2 = -(theta(1) + theta(2) * x1) / theta(3);
plot(x1, x2);



