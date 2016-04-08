% File: costLogisticPlot.m

x = -10:0.1:10;
h = 1 ./ (1 + exp(-x));

% first plot
figure;
costLogis = -log(h);
subplot(1,2,1);
plot(h, costLogis);
xlabel('h');
ylabel('cost');
title('if y = 1');
axis([-0.2 1.2 -0.2 10]);

% second plot
subplot(1,2,2);
costLogis2 = -log(1 - h);
plot(h, costLogis2);
xlabel('h');
ylabel('cost');
title('if y = 0');
axis([-0.2 1.2 -0.2 10]);

print -deps '../images/costLogisticPlot.eps'