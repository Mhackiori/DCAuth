dirinfo = dir();
dirinfo(~[dirinfo.isdir]) = [];  % Remove non-directories

subdirinfo = cell(length(dirinfo));
for K = 1 : length(dirinfo)
  thisdir = dirinfo(K).name;
  subdirinfo{K} = dir(fullfile(thisdir, '*.mat'));
end

subdirinfo(1, :) = [];
subdirinfo(1, :) = [];

for i = 1 : 4
    s = subdirinfo{i, 1};
    for j = 1 : length(s)

        disppp = ['[', string(i), '/4] ', '[', string(j), '/', string(length(s)), ']'];
        fprintf('%s',disppp);
        disp(' ');

        name = s(j).name;
        folder = s(j).folder;
        path = strcat(folder, '\');
        path = strcat(path, name);
        try
            data = load(path);
            field = erase(name, ".mat");
            field = strrep(field, '-', '_');
            field = strrep(field, '.', '_');
            field = field(find(~isspace(field)));
            d = extractfield(data, field);
            dd = d{1,1};
            ddd= removevars(dd,{'Step', 'StepTime', 'Temp1', 'VARx1', 'VARx10', 'VARx11', 'VARx12', 'VARx13', 'VARx14', 'VARx15', 'VARx2', 'VARx3', 'VARx4', 'VARx5', 'VARx6', 'VARx7', 'VARx8', 'VARx9', 'TestTime'});
            
            path2 = 'C:\Users\**username**\Downloads\';
            path2 = strcat(path2, field);
            path2 = strcat(path2, '.xlsx');
            try
                writetable(ddd, path2);
            catch
                % Nothing
            end
        catch
            % Nothing
        end
    end
end