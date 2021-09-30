%#ok<*AGROW>

close all; clear; clc;

base_path = "../data";
ref_base_path = "../data/ref_images";
excluded = [".", "..", "ref_images", "transformations", "other"];
data = {};

files = dir(base_path);
for i = 1:length(files)
    if files(i).isdir && ~any(strcmp(excluded, files(i).name))
        dir_data = {};
        dir_path = fullfile(base_path, files(i).name);
        images = dir(dir_path);
        
        for j = 1:length(images)
                if ~images(j).isdir
                    ref_path = fullfile(ref_base_path, ref_image(images(j).name));
                    meas_path = fullfile(dir_path, images(j).name);
                    dir_data = [dir_data, {compare(ref_path, meas_path)}];
                end
        end
        
        data = [data, {containers.Map([files(i).name], {dir_data})}]; 
    end
end

data = jsonencode(data);
fid = fopen(fullfile(base_path, "data.json"), "w");
if fid == -1; error("Cannot create JSON file"); end
fwrite(fid, data, "char");
fclose(fid);

py_command = "python fix_data_json.py";
[status, output] = system(py_command);
disp(output);

