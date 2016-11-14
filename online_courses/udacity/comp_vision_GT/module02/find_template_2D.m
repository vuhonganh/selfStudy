%% find template 2D 

function [yIndex, xIndex] = find_template_2D(template, img)
    % TODO: Find template in img and return [y x] location
    c = normxcorr2(template, img); % c will be a 2D matrix in this case
    % let's find the index where it is maximum
    [rawYidx, rawXidx] = find(c == max(c(:))); % flatten the 2D matrix c, find its max, and search for it
    % the match point is the last point of template matched region so
    % we need to reduce the offset
    yIndex = rawYidx - size(template, 1) + 1;  % y <-> row
    xIndex = rawXidx - size(template, 2) + 1;  % x <-> col
end
%endfunction

% uncomment if you use Octave
% pkg load image;

% img = imread('afreightim001.png');
% img = rgb2gray(img);
% templ = img(30:60,50:90);
% [yMatch, xMatch] = find_template_2D(templ, img);
% disp(yMatch);
% disp(xMatch);
