opencv_traincascade.exe -data data -vec positive_samples.vec -bg negative_samples.txt -numPos 1800 -numNeg 5400 -numStages 10 -w 40 -h 40 -minHitRate 0.99 -maxFalseAlarmRate 0.5 -mode ALL