z = -20:1:20;
g = 1 ./ (1 + exp(-z));
figure;
plot(z,g);
xlabel('z'); ylabel('g');
axis([-20 20 -0.5 1.5]);
print -deps 'sigmoid.eps'