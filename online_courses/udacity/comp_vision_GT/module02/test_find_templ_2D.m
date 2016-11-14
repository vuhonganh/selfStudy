img = imread('afreightim001.png');
img = rgb2gray(img);
templ = img(30:60,50:90);
[yMatch, xMatch] = find_template_2D(templ, img);
disp(yMatch);
disp(xMatch);

%subplot(1,2,1);
%hFig = figure;

hAx  = axes;
imshow(img,'Parent', hAx);
imrect(hAx, [xMatch, yMatch, size(templ,2), size(templ,1)]);
% imshow(templ);
