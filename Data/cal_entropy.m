
wts=ones(1,100)*0.01;

wts = wts/sum(wts);

ent(1) = sum(-wts.*log(wts));

wts = idcdf(random('norm',0,1,100,1));

ent(2) = sum(-wts.*log(wts));

wts = random('Poisson',1:6,1,6,100,1);

ent(3) = sum(-wts.*log(wts));