clc;clear all;close all;
base_pw = -45;
ax = 36;
ay = 27;
n_anchor = 20;

anchor = zeros(n_anchor,2);
cnt=1;
for ix = 1:5
    for iy = 1:4
        anchor(cnt,:)=[ix*6+random('Normal',0,3,1),iy*6+random('Normal',0,3,1)];
        cnt=cnt+1;
    end
end
anchor = anchor(randperm(n_anchor),:);

fid = fopen(['anchor',num2str(ax),'*',num2str(ay),'.txt'],'w');

for i=1:length(anchor)
    fprintf(fid,[num2str(i),',',num2str(anchor(i,1)),',']);
    fprintf(fid,[num2str(anchor(i,2)),'\r\n']);
end
fclose(fid);       

fingerprint = zeros(ax*ay*n_anchor,4);
cnt=1;
for ix=1:ax
    for iy=1:ay
        for ia = 1:n_anchor      
            d = norm([ix-1,iy-1]-anchor(ia,:),2);
            if d==0
                rss = base_pw;
            else
                rss = base_pw-20*log10(d);
            end
            fingerprint(cnt,:)=[ix-1,iy-1,ia,rss];
            cnt=cnt+1;
        end
    end
end

%%
fid = fopen(['fingerprint',num2str(ax),'*',num2str(ay),'.txt'],'w');
for i=1:length(fingerprint)
    for j=1:3
        fprintf(fid,[num2str(fingerprint(i,j)),',']);
    end
    fprintf(fid,[num2str(fingerprint(i,4)),'\r\n']);
end
fclose(fid);       
%%
X = fingerprint(:,1);
Y = fingerprint(:,2);
src = fingerprint(:,3);
mean_rssi = fingerprint(:,4);

for i_src=1:n_anchor
    index_i_src = find(src==i_src);
    X_slt = X(index_i_src);
    Y_slt = Y(index_i_src);
    mean_rssi_slt = mean_rssi(index_i_src);
    for i=1:length(X_slt)
        mean_3_rssi(X_slt(i)+1,Y_slt(i)+1)=mean_rssi_slt(i);
        
    end
        figure;
        imagesc(mean_3_rssi);
        title(['mean',num2str(i_src)]);
        %set(gca,'ydir','normal')
      
end