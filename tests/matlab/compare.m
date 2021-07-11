function [map] = compare(ref_path, meas_path)
    ref_image = imread(ref_path);
    meas_image = imread(meas_path);

    err = immse(meas_image, ref_image);
    peaksnr = psnr(meas_image, ref_image);
    ssimval = ssim(meas_image, ref_image);
    
    metrics = containers.Map(["mse", "psnr", "ssim"], {err, peaksnr, ssimval});
    map = containers.Map(["reference", "measured", "metrics"], {ref_path, meas_path, metrics});
end