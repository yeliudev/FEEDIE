for n = 1:1522

    inputPath = '/Volumes/Data/positive_samples/';
    outputPath = '/Volumes/Data/positive_samples_output/';
    filename = num2str(n);
    suffix = '.jpg';

    filePath = [inputPath,filename,suffix];
    fileOutputPath = [outputPath,filename,suffix];

    image = imread(filePath);
    grayImage = rgb2gray(image);
 
    imwrite(grayImage,fileOutputPath);
    display(n);

end
