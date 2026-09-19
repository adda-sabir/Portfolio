if exist('X','var') == 0
    X = [-0.2 40 1 5];
end    
[X] = fminsearch('idprev',X,[],tm,ym);
taille=15;

drawnow

