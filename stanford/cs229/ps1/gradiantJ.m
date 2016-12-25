function grad = gradiantJ(theta, Y, X)

% get number of data
m = size(X, 1);

% init grad
grad = zeros(size(X(1,:)));

for i = 1:m
    zi = Y(i) * X(i, :) * theta;
    grad = grad - 1/m * Y(i)*(1 - mySigmoid(zi)) * X(i,:);
end

% tranpose grad to column vector
grad = grad';