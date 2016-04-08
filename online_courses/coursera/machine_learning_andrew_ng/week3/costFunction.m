% File: costFunction.m
% the cost function J = (theta1 - 5)^2 + (theta2 - 5)^2;
% we write them in vector form and it also works! 
% The purpose of writing in vector form is to
% avoid duplicating code compute gradient elements

function [jVal, grad] = costFunction(theta)
	jVal = (theta - 5)' * (theta - 5);
	grad = 2 * (theta - 5);
end
