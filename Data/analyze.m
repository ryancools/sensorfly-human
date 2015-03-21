clc;clear all;close all;
folder = 'DrunkWalk/'
filename = 'data_m9_12_e1_a3_p100_i1_nr0.1_nv20_nt20.mat'

load([folder,filename])



data= reshape(record_list(1,:,:),size(record_list,2),size(record_list,3));

figure

for j=1:1
    data1 = data(find(data(:,2)==j),:);
    
   % data1 = data1(1:1800,:);
    
    error1 = zeros(length(data1),1);
    error2 = error1;
    for i=1:length(data1)
        error1(i,1) = norm(data1(i,3:4)-data1(i,5:6),2);
        error2(i,1) = norm(data1(i,3:4)-data1(i,7:8),2);
    end

    sig_cnt = data1(:,10);
    entropy = data1(:,11);
    time = data1(:,1);

    N = 3600;
    
%     figure
%     subplot(1,2,1)
%     plot(time(1:N),error1(1:N),'b');
%     xlabel('time(s)');ylabel('localization error');
%     title(['node ',num2str(j),' loc error']);
% 
%     subplot(1,2,2)
%     plot(time(1:N),entropy(1:N),'r');
%     xlabel('time(s)');ylabel('entropy');
%     title(['node ',num2str(j),' entropy']);
    %subplot(3,4,j+1)
    plot(time(1:N),error1(1:N),'b');hold on;
    plot(time(1:N),error2(1:N),'r');
    axis([0,N,0,100])
    title(['node ',num2str(j)]);

end

