% For Your Eyes Only part

% uncomment line below if using Octave
% pkg load image;

frizzy = imread('frizzy.png');
froomer = imread('froomer.png');
figure, imshow(frizzy), title('frizzy');
% imshow(froomer);

% TODO: Find edges in frizzy and froomer images
e_frizzy = edge(rgb2gray(frizzy), 'canny');
e_froomer = edge(rgb2gray(froomer), 'canny');
% imshow(e_frizzy);
% imshow(e_froomer);

common_edges = e_frizzy & e_froomer;
figure, imshow(common_edges), title('code');
