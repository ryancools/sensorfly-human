clc;clear all;

folder = '../ArenaMaps/';
fin = 'testbed.bmp';
fout ='testbed9_12.bmp'%'testbed29_38.bmp';

%image_in = imread([folder,fin]);

wid = 12+2;%27+2;
len = 9+2;%36+2;



image_tmp = zeros(len,wid);
image_tmp(1,:)=ones(1,wid);
image_tmp(end,:)=ones(1,wid);
image_tmp(:,1)=ones(len,1);
image_tmp(:,end)=ones(len,1);

%image_tmp = ones(len,wid)-image_tmp;

image_out =logical(image_tmp);
imwrite(image_out,[folder,fout]);



