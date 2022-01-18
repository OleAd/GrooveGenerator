function output = getMIR(input)
    addpath(genpath('MIRtoolbox1.8.1/'));
    mirwaitbar(0);
    beatspectrum = mean(mirgetdata(mirbeatspectrum(input)));
    pulse = mirgetdata(mirpulseclarity(input));
    novelty = mirgetdata(mirnovelty(input));
    aucNovel = cumtrapz(1:length(novelty), novelty);
    aucNovel = aucNovel(end);
    stdNovel = std(novelty);
    
    output = [beatspectrum, pulse, aucNovel, stdNovel];

return


getMIR(input)