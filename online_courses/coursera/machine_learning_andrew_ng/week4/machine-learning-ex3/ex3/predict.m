function p = predict(Theta1, Theta2, X)
%PREDICT Predict the label of an input given a trained neural network
%   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
%   trained weights of a neural network (Theta1, Theta2)

% Useful values
m = size(X, 1);
num_labels = size(Theta2, 1);

% You need to return the following variables correctly 
p = zeros(size(X, 1), 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Complete the following code to make predictions using
%               your learned neural network. You should set p to a 
%               vector containing labels between 1 to num_labels.
%
% Hint: The max function might come in useful. In particular, the max
%       function can also return the index of the max element, for more
%       information see 'help max'. If your examples are in rows, then, you
%       can use max(A, [], 2) to obtain the max for each row.
%

% Add collumn of 1 in X
inLayer = [ones(m, 1) X];

% The only one hidden layer named A1 can be computed by:
A1 = sigmoid(Theta1 * inLayer');

% Add row of 1 in A1
rowOne = ones(1, size(A1, 2));
A1 = [rowOne; A1];

% The result can be computed by:
outputLayer = sigmoid(Theta2 * A1);

[val, p] = max(outputLayer', [], 2);






% =========================================================================


end
