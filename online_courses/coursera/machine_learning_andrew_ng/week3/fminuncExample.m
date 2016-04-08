% File: fminuncExample.m

% fminunc is more sophisticated optimization method which is faster than our simple gradient descent
% Octave has it implemented in built-in library so we just know how to use them as following:
% declare options: set GradObj to on and max nb of iteration is 100
options = optimset('GradObj', 'on', 'MaxIter', 100);

% choose initial theta, we can see that we do not need to choose a learning rate alpha
initialTheta = zeros(2,1);

% call the fminunc
[optTheta, functionVal, exitFlag] = fminunc(@costFunction, initialTheta, options);

% display results
optTheta
functionVal
exitFlag