import numpy as np
from numpy import arange

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
    for i in range(len_x):
        C[i] = X[i] * Y[i]
    x = np.mean(X)
    y = np.mean(Y)
    c = np.mean(C)
    g = c / ((x * y))
    #g2 = (c - K * N)/((x-K) * (y-N))-(K / (x-K))-(N / (y-N))
    dx = (np.std(X)) / np.sqrt(len_x - 1)
    dy = (np.std(Y)) / np.sqrt(len_x - 1)
    dc = (np.std(C)) / np.sqrt(len_x - 1)
    dg = g * np.sqrt(((dx / x) ** 2) + ((dy / y) ** 2) + (dc / c) ** 2)
    eff_1 = 100 * (g - 1) * (x / A)
    deff1 = 100 * np.sqrt((x * dg / A) ** 2 + ((g - 1) * dx / A) ** 2)
    eff_2 = 100 * (g - 1) * (y / B)
    deff2 = 100 * np.sqrt((y * dg / B) ** 2 + ((g - 1) * dy / B) ** 2)

    with open(file_name, "a+") as fileVar:
        output = str(k) + " " + str(round(g, 8)) + " " + str(round(dg, 8)) + " " + str(round(x, 8)) + " " + \
                 str(round(y, 8)) + " " + str(round(eff_1, 8)) + " " + str(round(deff1, 8)) + " " + \
                 str(round(eff_2, 8)) + " " + str(round(deff2, 8)) + " " + "\n"
        fileVar.write(output)
    return g

q_APD = np.genfromtxt('C:/Users/Пользователь/Desktop/Лаба/Калибровки/405/Первые результаты по калибровке в аналоговом режиме и статья оптикс экспресс/многомод 50 + многомод 62.5/Работа с Фэу/Калибруем Оранжевый/Фэу 100ns 50mV g652800 (30min) (пошло в optics express)/m50out100nsD_90ns(30min)g652800(50mV)O.txt', 'float64')
q_PMT = np.genfromtxt('C:/Users/Пользователь/Desktop/Лаба/Калибровки/405/Первые результаты по калибровке в аналоговом режиме и статья оптикс экспресс/многомод 50 + многомод 62.5/Работа с Фэу/Калибруем Оранжевый/Фэу 100ns 50mV g652800 (30min) (пошло в optics express)/m50out100nsD_90ns(30min)g652800(50mV)F.txt', 'float64')
for k in arange(0, 100, 1):

    with open('C:/Users/Пользователь/Desktop/3.txt', "w+") as file:
        for i in range(q_APD.size):
            if q_APD[i] > k:
                file.write(str(q_PMT[i])+'\n')
            else:
                file.write('0'+'\n')

        my_file1 = "C:/Users/Пользователь/Desktop/Лаба/Калибровки/405/Первые результаты по калибровке в аналоговом режиме и статья оптикс экспресс/многомод 50 + многомод 62.5/Работа с Фэу/Калибруем Оранжевый/Фэу 100ns 50mV g652800 (30min) (пошло в optics express)/m50out100nsD_90ns(30min)g652800(50mV)O.txt"
        my_file2 = "C:/Users/Пользователь/Desktop/3.txt"

        file_name = "C:/Users/Пользователь/Desktop/file_name.txt"

    fileVar = open(file_name, "a+")
    fileVar.close()

    K = 4e-05
    N = 0
    X = delete_noize_new(my_file1, 0, 99999, 0, 0, 0, 0, K, 'new_file1.txt')
    Y = delete_noize_new(my_file2, 0, 99999, 0, 0, 0, 0, N, 'new_file2.txt')
    g = G(X, Y, 1361, 99, 0, 0) # последние два числа это найденый ранее уровень фона
    print(k, g)
