import numpy as np


def delete_noize_new(my_file, E, B, C, D, F, K, new_file, w=False):
    f = open(my_file)

    A = []
    for line in f:
        a = float(line)
        if ((a > E and B > a) or (a > C and D > a) or (a > F and K > a)):
            A.append(a)
        else:
            A.append(0.0)
    B = np.copy(A)
    if w:
        np.savetxt(new_file, B, fmt='%f')
    return B


def G(X, Y, A, B, N1, N2):
    len_x = len(X)
    C = np.linspace(0, 0, len_x)
    for i in range(len_x):
        C[i] = X[i] * Y[i]
    x = np.mean(X - N1)
    y = np.mean(Y - N2)
    c = np.mean(C)
    dx = np.std(X - N1)
    dy = np.std(Y - N2)
    dc = np.std(C)
    g = c / (x * y)
    dx = (np.std(X)) / np.sqrt(len_x - 1)
    dy = (np.std(Y)) / np.sqrt(len_x - 1)
    dc = (np.std(C)) / np.sqrt(len_x - 1)
    dg = g * np.sqrt(((dx / x) ** 2) + ((dy / y) ** 2) + (dc / c) ** 2)
    # dg = np.sqrt( (dc/x*y)**2 + (c*dy/(x*y**2))**2 + (c*dx/(y*x**2))**2 )

    eff_1 = 100 * (g - 1) * (x / A)
    deff1 = 100 * np.sqrt((x * dg / A) ** 2 + ((g - 1) * dx / A) ** 2)
    eff_2 = 100 * (g - 1) * y / B
    deff2 = 100 * np.sqrt((y * dg / B) ** 2 + ((g - 1) * dy / B) ** 2)

    with open(file_name, "a+") as fileVar:
        output = str(k) + " " + str(round(g, 5)) + " " + str(round(dg, 5)) + " " + str(round(x, 5)) + " " + \
                 str(round(y, 5)) + " " + str(round(eff_1, 5)) + " " + str(round(deff1, 5)) + " " + \
                 str(round(eff_2, 5)) + " " + str(round(deff2, 5)) + "\n"
        fileVar.write(output)

    return c / (x * y)

q_APD = np.genfromtxt('C:/Users/ahito/Desktop/Взаимные калибровки/строб 900 от мощности + много шума/1.25m31s900O.txt', 'float64')
q_PMT = np.genfromtxt('C:/Users/ahito/Desktop/Взаимные калибровки/строб 900 от мощности + много шума/1.25m31s900F.txt', 'float64')
for k in range(572, 574, 2):
    # q_APD_1 = np.array([], 'float64')
    # q_PMT_1 = np.array([], 'float64')
    with open('C:/Users/ahito/Desktop/3.txt', "w+") as file:
        for i in range(q_APD.size):
            if q_APD[i] > k:
                # q_PMT_1 = np.append(q_PMT_1, q_PMT[i])
                file.write(str(q_PMT[i])+'\n')
            else:
                file.write('0'+'\n')

        my_file1 = "C:/Users/ahito/Desktop/Взаимные калибровки/строб 900 от мощности + много шума/1.25m31s900O.txt"
        # my_file2 = "C:/Users/Пользователь/Desktop/Лаба/калибровки/многомод 50 + многомод 62.5/Работа с Фэу/Калибруем Оранжевый/Фэу 100ns 50mV g652800 (30min)/m50out100nsD_90ns(30min)g652800(50mV)F.txt"

        my_file2 = "C:/Users/ahito/Desktop/3.txt"

        file_name = "C:/Users/ahito/Desktop/file_name.txt"

    fileVar = open(file_name, "a+")
    fileVar.close()

    # for j in range(0, 1, 1):
    # green
    X = delete_noize_new(my_file1, 1340, 10000, 0, 0, 0, 0, 'new_file1.txt')
    # orange
    Y = delete_noize_new(my_file2, 0, 99999, 0, 0, 0, 0, 'new_file2.txt')
    g = G(X, Y, 1144, 1400, 0, 0) # последние два числа это найденное ранее Zшумовой

    # print(j)
    print(k)