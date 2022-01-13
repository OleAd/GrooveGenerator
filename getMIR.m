function output = getMIR(input)
    addpath(genpath('MIRtoolbox1.8.1/'));
    mirwaitbar(0);
    beatspectrum = mean(mirgetdata(mirbeatspectrum(input)));
    pulse = mirgetdata(mirpulseclarity(input));
    novelty = mirgetdata(mirnovelty(input));
    aucNovel = trapz(1:length(novelty), novelty);
    stdNovel = std(novelty);
    
    output = [beatspectrum, pulse, aucNovel, stdNovel];

return


getMIR(input)