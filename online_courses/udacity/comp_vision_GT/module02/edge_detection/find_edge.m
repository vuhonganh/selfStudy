%uncomment line below if using Octave
% pkg load image;

% load hexagon image and convert to double type
% range [0, 1] for convenience and avoiding
% big numerical results
img = double(imread('octagon.png'))/225.0;


% compute x, y gradients using imgradientxy
% this returns a pair of matrices (grad in x and grad in y)
[gx, gy] = imgradientxy(img, 'sobel'); 

% need to add an offset +4 because under range [0,1] we get a range value
% in [-4, 4]
% then need to normalise by 8 as matlab does not normalise
% imshow((gx + 4)/8); % now we scale back to [0, 1]
% alternatives: 
% imshow(gx, [-4, 4]); imshow(gx, []); 

% Obtain gradient magnitude and direction:
[gmag, gdir] = imgradient(gx, gy);
% again max value of gmag is sqrt(4^2 + 4^2) = 4*sqrt(2)
% we scale down to have [0, 1] output image
% imshow(gmag / (4 * sqrt(2)));  
% imshow((gdir + 180.) / 360.);  % gdir range from -180 to +180

% Find pixels with desired gradient direction
my_grad = select_gdir(gmag, gdir, 1, 30, 60); % 45 +/- 15
imshow(my_grad);

