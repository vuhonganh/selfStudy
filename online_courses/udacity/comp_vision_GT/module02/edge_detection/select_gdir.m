function result = select_gdir(gmag, gdir, mag_min, angle_low, angle_high)
% Find and return pixels that fall within the desired angle range
% with magniture >= mag_min to avoid noise
result = gmag >= mag_min & gdir >= angle_low & gdir <= angle_high;
end


% old version: not very efficient and profesional
% function result = select_gdir(gmag, gdir, mag_min, angle_low, angle_high)
% % Find and return pixels that fall within the desired angle range
% % with magniture >= mag_min to avoid noise
% result = gdir;  % note that gdir normally in range [-180, +180]
% for r = 1:size(gdir, 1)
%     for c = 1:size(gdir, 2)
%         if gmag(r, c) >= mag_min && angle_low <= gdir(r, c) && gdir(r, c) <= angle_high
%             result(r, c) = 1;
%         else
%             result(r, c) = 0;
%         end
%     end
% end
% end