function plotData(X, y)
%PLOTDATA Plots the data points X and y into a new figure 
%   PLOTDATA(x,y) plots the data points with + for the positive examples
%   and o for the negative examples. X is assumed to be a Mx2 matrix.

% Create New Figure
figure; hold on;

% ====================== YOUR CODE HERE ======================
% Instructions: Plot the positive and negative examples on a
%               2D plot, using the option 'k+' for the positive
%               examples and 'ko' for the negative examples.
%

posiElem = find(y == 1);
negaElem = find(y == 0);
plot(X(posiElem, 1), X(posiElem, 2), 'b+');

plot(X(negaElem, 1), X(negaElem, 2), 'or');






% =========================================================================



hold off;

end
