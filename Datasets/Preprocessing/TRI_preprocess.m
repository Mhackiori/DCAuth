dirinfo = dir();
dirinfo(~[dirinfo.isdir]) = [];  % Remove non-directories

subdirinfo = cell(length(dirinfo));
for K = 1 : length(dirinfo)
  thisdir = dirinfo(K).name;
  subdirinfo{K} = dir(fullfile(thisdir, '*.mat'));
end

subdirinfo(1, :) = [];
subdirinfo(1, :) = [];


for i = 1 : 8
    s = subdirinfo{i, 1};
    for j = 1 : length(s)
        name = s(j).name;
        folder = s(j).folder;
        path = strcat(folder, '\');
        path = strcat(path, name);

        data = load(path);
        field = erase(name, ".mat");
        d = extractfield(data, field);
        dd = d{1,1};

        for k = 2 : length(dd)
            disppp = ['[', string(i), '/8] ', '[', string(j), '/', string(length(s)), '] ', '[', string(k), '/', string(length(dd)), '] '];
            fprintf('%s',disppp);
            disp(' ');
            ddd = dd{k, 3};
            path2 = 'C:\Users\**username**\Downloads\';
            path2 = strcat(path2, field);
            path2 = strcat(path2, '_');
            lll = k-1;
            path2 = strcat(path2, string(lll));
            path2 = strcat(path2, '.xlsx');
            try
                writetable(ddd, path2);
            catch
                % Nothing
            end
        end

    end
end