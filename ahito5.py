import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

m = input()
# def log_hist(x):
#     f = plt.figure()
#     f.set_figwidth(20)
#     f.set_figheight(10)
#     plt.title(' ')  # заголовок
#     plt.grid()  # сетка
#     plt.rc('axes', labelsize=15)  # размер чиселок у осей
#     plt.yscale('log')
#     plt.hist(x, bins=1000)

def delete_noize_new(my_file, E, B, C, D, F, K, N, new_file, w=False):
    f = open(my_file)

    A = []
    for line in f:
        a = float(line)
        if ((a > E and B > a) or (a > C and D > a) or (a > F and K > a)):
            A.append(a - N)
        else:
            A.append(0.0)
    B = np.copy(A)
    if w:
        np.savetxt(new_file, B, fmt='%f')
    return B

def G(X, Y, A, B, K, N):
    len_x = len(X)
    C = np.linspace(0, 0, len_x)
    for p in range(0, 1, 1):
        for i in range(len_x):
            C[i] = X[i-p] * Y[i]
        x = np.mean(X)
        y = np.mean(Y)
        c = np.mean(C)
        g = c / ((x) * (y))
        g2 = (c - K * N)/((x-K) * (y-N))-(K / (x-K))-(N / (y-N))
        XX = x * X[i] / Y[i]
        alpha = X[i] / Y[i]
        NRF = (np.var(XX - Y) / np.mean(XX + Y))
        eff_1 = (x / A) * (g - 1)
        eff_2 = (y / B) * (g - 1)
        CN = 10000000 * (1 / (g - 1)) / 5 #поток
        Ks = 0.39
        chu = y / (CN * Ks)

        dx = (np.std(X)) / np.sqrt(len_x - 1)
        dy = (np.std(Y)) / np.sqrt(len_x - 1)
        dc = (np.std(C)) / np.sqrt(len_x - 1)
        dg = g * np.sqrt(((dx / x) ** 2) + ((dy / y) ** 2) + (dc / c) ** 2)
        dNRF = np.sqrt(((dx / x) ** 2) + ((dy / y) ** 2)) * NRF
        dCN = CN * np.sqrt((dg/g) ** 2)
        dchu = chu * np.sqrt((dCN/CN) ** 2 + (dy/y) ** 2)

        deff1 = np.sqrt((x * dg / A) ** 2 + (g * dx / A) ** 2)
        deff2 = np.sqrt((y * dg / B) ** 2 + ((g * dy / B) ** 2))


        with open(file_name, "a+") as fileVar:
            output = str(m) + " " + str(round(g, 7)) + " " + str(round(dg, 7)) + " " + str(round(g2, 7)) + " " + \
                     str(round(x, 7)) + " " + str(round(dx, 7)) + " " + \
                     str(round(y, 7)) + " " + str(round(dy, 7)) + " " + \
                     str(round(c, 7)) + " " + str(round(dc, 7)) + " " + \
                     str(round(NRF, 15)) + " " + str(round(dNRF, 15)) + " " + str(round(alpha, 5)) + " " +\
                     str(round(CN, 7)) + " " + str(round(dCN, 7)) + " " + \
                     str(round(chu, 15)) + " " + str(round(dchu, 15)) + " " + \
                     str(round(eff_1, 7)) + " " + str(round(deff1, 7)) + " " + \
                     str(round(eff_2, 7)) + " " + str(round(deff2, 7)) + " " + "\n"
            fileVar.write(output)

my_file1 = "C:/Users/Пользователь/Desktop/ПР/52 набор данных збс/Results52/21mWNE.txt"
my_file2 = "C:/Users/Пользователь/Desktop/ПР/52 набор данных збс/Results52/21mWNO.txt"

file_name = "C:/Users/Пользователь/Desktop/file_name.txt"

fileVar = open(file_name, "a+")
fileVar.close()

K = 0.0585472
N = 0.0406547

X = delete_noize_new(my_file1, -1, 1, 0, 0, 0, 0, K, 'new_file1.txt') #последнее число шум
Y = delete_noize_new(my_file2, -1, 1, 0, 0, 0, 0, N, 'new_file2.txt') #последнее число шум
g = G(X, Y, 4630, 3841, K, N)


# g2 = SDVGcorr(X, Y, 0, 0)
# plt.show()
# for i in range(2, 3):
#     filename1 = filesF[i]
#     filename = filesO[i]
#     # лфд - O
#     X = delete_noize_new(filename, 762, 999999, 0, 0, 0, 0, 0.08832618918734232, 'new_file1.txt')  # 0.08832618918734232
#     # фэу - F
#     Y = delete_noize_new(filename1, 0, 9999999, 0, 0, 0, 0, 354.58698447447375, 'new_file2.txt')  # 354.58698447447375
#     g2 = SDVGcorr(X, Y, -100, 100)
#     # g = G(X, Y, 1361, 70)
#
# plt.show()