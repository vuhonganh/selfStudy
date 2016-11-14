%% FIRST OF ALL: 
%% NEED TO GO TO THIS DIRECTORY TO READ FILE

pkg load image;

%img = imread('4.1.07.tiff');
img = imread('afreightim001.png');
%imshow(img);



%% Explore Filtering at Borders: 
% create gaussian filter
filter_size = 20;
filter_sigma = 2;
filter = fspecial('gaussian', filter_size, filter_sigma);


% apply it, specifying an edge parameter (ie border)
% smoothed = imfilter(img, filter, 0); % fill border with black
smoothed = imfilter(img, filter, 'symmetric'); 
imshow(smoothed);


