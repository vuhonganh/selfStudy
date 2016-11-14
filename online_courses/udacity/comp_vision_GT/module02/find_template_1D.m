% cach 1
%function index = find_template_1D(t, s)
%index = -1;
%len_t = length(t);
%len_s = length(s);
%for i = 1:len_s - len_t + 1
%  if s(i:i+len_t-1) == t
%    index = i;
%    %disp(i);
%  endif
%endfor
%endfunction

% cach 2

function index = find_template_1D(t, s)
  disp('hello');
  pkg load image;
  c = normxcorr2(t, s);
  [maxValue rawIndex] = max(c);
  disp(rawIndex);
  index = rawIndex - size(t, 2) + 1;
  disp(index);
endfunction



% test data below should give index = 5 as output
%s = [-1 0 0 1 1 1 0 -1  -1 ];
%t = [1 1 0];
%index = find_template_1D(t, s);
%disp(index);