% Median filter is non linear operator
% but it's good to deal with salt & pepper noise

pkg load image;

img = imread('afreightim001.png');
img = rgb2gray(img);
subplot(2,2,1);
imshow(img);


% add salt & pepper noise:
noisy_img = imnoise(img, 'salt & pepper', 0.02);
subplot(2,2,2);
imshow(noisy_img);

% apply a median filter
median_filtered = medfilt2(noisy_img);
subplot(2,2,3);
imshow(median_filtered);
