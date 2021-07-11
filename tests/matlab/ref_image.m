function [ref_path] = ref_image(image_path)
    match = "_" + digitsPattern;
    ref_path = erase(image_path, match);
end

