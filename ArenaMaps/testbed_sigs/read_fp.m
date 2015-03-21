clc;clear all;close all;

N = 5000;
final_data = zeros(N,5);
mean_std_data = zeros(N,5);
cnt=1;
cnt_mean = 1;
output='start'
for i_file = 0:8
   file = ['Row',num2str(i_file),'.txt'];
   rawdata = importdata(file);
   time_raw = rawdata(:,1);
   X_raw = rawdata(:,2);
   Y_raw = rawdata(:,3);
   source_raw = rawdata(:,4);
   rssi_raw = -rawdata(:,5);
   i_x = i_file;
   
   for i_y = 0:11
        index_i_y = find(Y_raw==i_y);
        if (isempty(index_i_y))
            output='missing!'
            return
        end
        slt_source = source_raw(index_i_y);
        [aaa,index_final]=sort(slt_source,'ascend');
        time = time_raw(index_i_y(index_final));
        X = X_raw(index_i_y(index_final));
        Y = Y_raw(index_i_y(index_final));
        source = source_raw(index_i_y(index_final));
        rssi = rssi_raw(index_i_y(index_final));
        final_data(cnt:cnt+length(X)-1,:)=[time,X,Y,source,rssi];
        cnt = cnt+length(X);
        
        for i_src = 1:4
            slt_src=find(source==i_src);
            mean_std_data(cnt_mean,1) = X(1);
            mean_std_data(cnt_mean,2) = Y(1);
            mean_std_data(cnt_mean,3) = i_src;
            mean_std_data(cnt_mean,4) = mean(rssi(slt_src));
            mean_std_data(cnt_mean,5) = std(rssi(slt_src));
            cnt_mean = cnt_mean+1;  
        end
    end
end
final_data = final_data(1:cnt-1,:);
save('fingerprint.mat','final_data');
mean_std_data = mean_std_data(1:cnt_mean-1,:);
save('fingerprint_mean.mat','mean_std_data');
%%
X = final_data(:,2);
Y = final_data(:,3);
src = final_data(:,4);
rssi = final_data(:,5);
for i_src = 1:4
    index_i_src = find(src==i_src);
    figure;
    plot3(X(index_i_src),Y(index_i_src),rssi(index_i_src),'*')
    title(num2str(i_src));
end
%%
X = mean_std_data(:,1);
Y = mean_std_data(:,2);
src = mean_std_data(:,3);
mean_rssi = mean_std_data(:,4);
std_rssi = mean_std_data(:,5);
for i_src=1:4
    index_i_src = find(src==i_src);
    X_slt = X(index_i_src);
    Y_slt = Y(index_i_src);
    mean_rssi_slt = mean_rssi(index_i_src);
    std_rssi_slt = std_rssi(index_i_src);
    for i=1:length(X_slt)
        mean_3_rssi(Y_slt(i)+1,X_slt(i)+1)=mean_rssi_slt(i);
        std_3_rssi(Y_slt(i)+1,X_slt(i)+1)=std_rssi_slt(i);
        
    end
        figure;
        imagesc(mean_3_rssi);
        title(['mean',num2str(i_src)]);
        set(gca,'ydir','normal')
        figure;
        imagesc(std_3_rssi);
        title(['std',num2str(i_src)]);
        set(gca,'ydir','normal')
end
%%
fid = fopen('fingerprint.txt','a+');
for i=1:length(mean_std_data)
    for j=1:3
        fprintf(fid,[num2str(mean_std_data(i,j)),',']);
    end
    fprintf(fid,[num2str(mean_std_data(i,4)),'\r\n']);
end
fclose(fid);
