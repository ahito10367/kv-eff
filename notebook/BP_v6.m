clc, clear

mkdir('Results') % Создание папки, куда буду записываться файлы, можно изменить название в формате folder\

[fileName, filePath] = uigetfile('*.txt', MultiSelect='on'); % Выберите файл для импорта
% load tmpData.mat
% load tmpDataAll.mat

delete(gcp('nocreate'))
ParP = parpool("Threads", 4); % Запуск параллеьного пула. Число = кол-во потоков
%%

% Тут вводить ключевые параметры -----------------------------------------
blockSize = 2e2; % размер блока для анализа максимумов распределения
meanCurrentX = 4630;
meanCurrentY = 3841;

saveFlag = false; % Сохранение X и Y без шума

GdataFileName = "Gdata.txt"; % Название файла с различными параметрами
DataFilePrepare(GdataFileName); % Поздание файла с параметрами
GdataHeader = GdataFormat(fileName); % Подготовка "хедеров"

%% MAIN body

tic
for i = [length(fileName) 1:length(fileName)-1]
    % Загрузка данных в оперативную память
    ds = tabularTextDatastore(string(filePath)+string(fileName{i}));
    fData = table2array(readall(ds, "UseParallel",true));

    % Вычисление максимумов в блоках
    [Xmaxes,Ymaxes] = findMaxesInBins(blockSize, fData);
    %[Xmaxes,Ymaxes] = BUGGED_findMaxesInBins(blockSize, fData); % Прога с опечаткой

    % Вычисление шума из файла shum.txt
    if i == length(fileName)
        [Xnoise, Ynoise] = getNoiseValue(Xmaxes, Ymaxes);
    end

    % Сохраняю Xnew/Ynew в файл "Название_исходиника_NO/NE.txt'
    saveLikeTxt(Xmaxes, fileName{i}(1:end-4)+"NO.txt")
    saveLikeTxt(Ymaxes, fileName{i}(1:end-4)+"NE.txt")
    
    XmetaData = CheckFile(fileName{i}, "X");
    YmetaData = CheckFile(fileName{i}, "Y");

    if i == length(fileName)
        Xx = DeleteNoise(XmetaData, -1, 1, 0, 0, 0, 0, 0, "X"+string(GdataHeader(i)), saveFlag); %последнее число шум
        Yy = DeleteNoise(YmetaData, -1, 1, 0, 0, 0, 0, 0, "Y"+string(GdataHeader(i)), saveFlag); %последнее число шум
        CalcG(Xx, Yy, meanCurrentX, meanCurrentY, 0, 0, GdataFileName, GdataHeader(i));
    else
        Xx = DeleteNoise(XmetaData, -1, 1, 0, 0, 0, 0, Xnoise, "X"+string(GdataHeader(i)), saveFlag); %последнее число шум
        Yy = DeleteNoise(YmetaData, -1, 1, 0, 0, 0, 0, Ynoise, "Y"+string(GdataHeader(i)), saveFlag); %последнее число шум
        CalcG(Xx, Yy, meanCurrentX, meanCurrentY, Xnoise, Ynoise, GdataFileName, GdataHeader(i));
    end
end
toc

delete(ParP) % Закрытие параллельного пула

Gdata = getGdata(GdataFileName);
%%
FIG.f6 = figure(6); FIG.f6.WindowStyle = "docked";
plot(Gdata.Power, Gdata.g, 'x-r'), grid on
xlabel("Power"), ylabel("g")

FIG.f7 = figure(7); FIG.f7.WindowStyle = "docked";
plot(Gdata.Power, Gdata.x, 'x-r',...
     Gdata.Power, Gdata.y, '*-b'), grid on
xlabel("Power"), ylabel("x,y")
legend('x','y')

FIG.f8 = figure(8); FIG.f8.WindowStyle = "docked";
plot(Gdata.Power, Gdata.NRF, 'x-r'), grid on
xlabel("Power"), ylabel("NRF")

% FIG.f1 = figure(1); FIG.f1.WindowStyle = "docked";
% histogram(Xmaxes, length(Xmaxes)), grid on
% title("Xmaxes")
% FIG.f2 = figure(2); FIG.f2.WindowStyle = "docked";
% histogram(Ymaxes, length(Ymaxes)), grid on
% title("Ymaxes")
% FIG.f3 = figure(3); FIG.f3.WindowStyle = "docked";
% histogram(Xx, length(Xx)), grid on
% title("XwoNoise")
% FIG.f4 = figure(4); FIG.f4.WindowStyle = "docked";
% histogram(Yy, length(Yy)), grid on
% title("YwoNoise")

%%

clear blockSize saveFlag GdataFileName
% clear Xmaxes Ymaxes Xx Yy
clear GdataHeader fData
clear XmetaData YmetaData
clear ans i 

%% Functions block --------------------------------------------------------

function [] = DataFilePrepare(saveFileName)
    outputArray = ["Power(mW)", "g", "dg", "x", "dx", "y", "dy", "c",...
                   "dc", "alpha" "NRF", "dNRF", "CN", "dCN", "chu", "dchu",...
                   "eff_1", "deff_1", "eff_2", "deff_2"];
    fileID = fopen(saveFileName,'wt');
    formatSpec = '%13s\t';
    fprintf(fileID, formatSpec, outputArray');
    fclose(fileID);
end

function [output] = GdataFormat(input)
    output = zeros(length(input),1);
    for j = 1:length(input)-1
        for i = 1:length(input{j})-1
            if input{j}(i:i+1) == "mW"
                output(j) = str2double(input{j}(1:i-1));
                break
            end
        end
    end
end

function [Xnoise, Ynoise] = getNoiseValue(Xmaxes, Ymaxes)
    Xnoise = mean(Xmaxes);
    Ynoise = mean(Ymaxes);
end

function [] = saveLikeTxt(inputArray, fileName)
    formatSpec = '%f\n';
    fileID = fopen(string(cd)+"\Results\"+fileName,'wt');
    fprintf(fileID, formatSpec, inputArray);
    fclose(fileID);
end

function [output] = CheckFile(fileName, ID)
    if ID == "X"
        output = "Results\"+string(fileName(1:end-4))+"NO.txt";
    elseif ID == "Y"
        output = "Results\"+string(fileName(1:end-4))+"NE.txt";
    end
end

function [outputX, outputY] = findMaxesInBins(blockSize, fData)
    fLen = size(fData, 1);
    blocksNum = floor(fLen/blockSize)+1;
    outputX = zeros(blocksNum, 1);
    outputY = zeros(blocksNum, 1);
    for i = 1:blockSize:(fLen-blockSize)
        Xmax = fData(i, 1);
        Ymax = fData(i, 2);
        for j = i:i+blockSize-1
            if fData(j, 1)>Xmax
                Xmax = fData(j, 1);
            end
            if fData(j, 2)>Ymax
                Ymax = fData(j, 2);
            end
        end
        outputX((i-1)/blockSize+1) = Xmax;
        outputY((i-1)/blockSize+1) = Ymax;
    end
end

function [outputX, outputY] = BUGGED_findMaxesInBins(blockSize, fData)
    fLen = length(fData{1});
    blocksNum = floor(fLen/blockSize)+1;
    outputX = zeros(blocksNum, 1);
    outputY = zeros(blocksNum, 1);
    for i = 1:blockSize:(fLen-blockSize)
        Xmax = fData{1}(blockSize*floor(i/(blockSize+1))+1);
        Ymax = fData{2}(blockSize*floor(i/(blockSize+1))+1);% here
        for j = i:i+blockSize-1
            if fData{1}(j+1)>Xmax
                Xmax = fData{1}(j+1);
            end
            if fData{2}(j+1)>Ymax
                Ymax = fData{2}(j+1);
            end
        end
        outputX((i-1)/blockSize+1) = Xmax;
        outputY((i-1)/blockSize+1) = Ymax;
    end
end

function [tData] = DeleteNoise(fileMetaData, E, B, C, D, F, K, N, saveFileName, saveFlag)
    fID = fopen(fileMetaData);
    fData = textscan(fID, '%f32');
    fclose(fID);
    tData = fData{1};
    
    for i = 1:length(tData)
        if ((tData(i) > E && B > tData(i)) || (tData(i) > C && D > tData(i)) || (tData(i) > F && K > tData(i)))
            tData(i) = tData(i)-N;
        else
            tData(i) = 0;
        end
    end
    
    if saveFlag
        saveLikeTxt(tData, "woNoise"+saveFileName+"mW.txt")
    end
end

function [outputArray] = CalcG(X,Y,A,B,K,N,saveFileName,header)
xLen = length(X);
C = zeros(xLen, 1);

for p = 0
    for i = 1:xLen
        C(i) = X(i-p) * Y(i);
    end
    x = mean(X);
    y = mean(Y);
    c = mean(C);

    g = c / (x * y);
    % g2 = (c - K*N)/((x-K) * (y-N))-(K / (x-K)) - (N / (y-N));

    XX = Y * x/y;
    alpha = x/y;
    NRF = var(XX-X) / mean(XX + x);
    eff_1 = (x /A) * (g-1);
    eff_2 = (y /B) * (g-1);

    CN = 10000000 * (1 / (g - 1)) / 5; %поток

    Ks = 0.39;

    chu = y/(CN * Ks);

    dx = std(X) / sqrt(xLen-1);
    dy = std(Y) / sqrt(xLen-1);
    dc = std(C) / sqrt(xLen-1);

    dg = g * sqrt((dx/x)^2 + (dy/y)^2 + (dc/c)^2);
    dNRF = NRF * sqrt((dx/x)^2 + (dy/y)^2);

    dCN = CN * sqrt((dg/g)^2);

    dchu = chu * sqrt( (dCN/CN)^2 + (dy/y)^2);

    deff_1 = sqrt( (x * dg/A)^2 + (g * dx/A)^2 );
    deff_2 = sqrt( (y * dg/B)^2 + (g * dy/B)^2 );

    outputArray = string([header, g, dg, x, dx, y, dy, c,...
                   dc, alpha, NRF, dNRF, CN, dCN, chu, dchu,...
                   eff_1, deff_1, eff_2, deff_2]);
    formatSpec = '%.10f\t';
    fileID = fopen(saveFileName,'at');
    fprintf(fileID, '\n');
    fprintf(fileID, formatSpec, outputArray);
    fclose(fileID);
end
end

function GdataStruct = getGdata(GdataFileName)

GdataMat = readmatrix(GdataFileName);

GdataStruct.Power = GdataMat(:,1);
GdataStruct.g = GdataMat(:,2);
GdataStruct.x = GdataMat(:,5);
GdataStruct.y = GdataMat(:,7);
GdataStruct.c = GdataMat(:,9);
GdataStruct.c = GdataMat(:,9);
GdataStruct.NRF = GdataMat(:,11);

end
