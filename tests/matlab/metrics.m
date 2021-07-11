close all; clear; clc;

base_path = "../data";
ref_base_path = "../data/ref_images";
excluded = [".", "..", "ref_images"];

files = dir(base_path);
for i = 1:length(files)
    if files(i).isdir && ~any(strcmp(excluded, files(i).name))
        data = {};
        dir_path = fullfile(base_path, files(i).name);
        images = dir(dir_path);
        
        for j = 1:length(images)
                if ~images(j).isdir
                    ref_path = fullfile(ref_base_path, ref_image(images(j).name));
                    meas_path = fullfile(dir_path, images(j).name);
                    data = [data, {compare(ref_path, meas_path)}]; %#ok<AGROW>
                end
        end
        
        data = jsonencode(data);
        fid = fopen(fullfile(base_path, files(i).name, "data.json"), "w");
        if fid == -1, error("Cannot create JSON file"); end
        fwrite(fid, data, "char");
        fclose(fid);
    end
end

