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
    global NRF
    len_x = len(X)
    C = np.linspace(0, 0, len_x)
    for p in range(0, 1, 1):
        for i in range(len_x):
            # C[i] = (X[i] - N1) * (Y[i] - N2)
            C[i] = X[i] * Y[i-p]
        x = np.mean(X) - N1
        y = np.mean(Y) - N2
        x1 = np.mean(X)
        y1 = np.mean(Y)
        c = np.mean(C)
        #UU = N1*N2*(y/N2 + x/N1 - 1)
        g = c / (x * y)
        g2 = (x1 * y1) / (x * y)
        a1 = N1 / np.mean(X)
        a2 = N2 / np.mean(Y)
        csi = a1 * a2 - a1 - a2
        dx = (np.std(X)) / np.sqrt(len_x - 1)
        dy = (np.std(Y)) / np.sqrt(len_x - 1)
        dc = (np.std(C)) / np.sqrt(len_x - 1)
        dg = g * np.sqrt(((dx / x) ** 2) + ((dy / y) ** 2) + (dc / c) ** 2)
        XX = X*y/x
        alpha = y/x
        # dg = np.sqrt((dc/x*y)**2 + (c*dy/(x*y**2))**2 + (c*dx/(y*x**2))**2)
        Q = 52 # средний заряд
        NRF = (np.var(XX-Y)/np.mean(XX+Y))/Q
        fon = 1 # считается когда мы считаем сдвинутое g2 (в C меняем i на i-1 например) по умолчанию 1

        eff_1 = 100 * (x / A) * ((g - fon + 1) - 1) # где 1 это постамент у временной зависимости и может быть вычесленно как сдвиг х относительно у
        deff1 = 100 * np.sqrt((x * dg / A) ** 2 + (g * dx / A) ** 2)
        eff_2 = 100 * (y / B) * ((g - fon + 1) - 1) # где 1 это постамент у временной зависимости и может быть вычесленно как сдвиг х относительно у
        deff2 = 100 * np.sqrt((y * dg / B) ** 2 + ((g * dy / B) ** 2))
        dNRF = np.sqrt(((dx / x) ** 2) + ((dy / y) ** 2)) * NRF

        with open(file_name, "a+") as fileVar:
            output = str(k) + " " + str(round(g, 5)) + " " + str(round(dg, 5)) + " " + str(round(g2, 5)) + " " + str(round(fon, 5)) + " " + \
                     str(round(x, 5)) + " " + str(round(y, 5)) + " " + \
                     str(round(eff_1, 5)) + " " + str(round(deff1, 5)) + " " + \
                     str(round(eff_2, 5)) + " " + str(round(deff2, 5)) + " " + \
                     str(round(NRF, 5)) + " " + str(round(dNRF, 5)) + " " + str(round(alpha, 5)) + " " +\
                     str(round(a1, 5)) + " " + str(round(a2, 5)) + " " + str(round(csi, 5)) + "\n"
            fileVar.write(output)

    return g

q_APD = np.genfromtxt('C:/Users/Пользователь/Desktop/Лаба/Калибровки/405/Продолжение работы по калибровки аналоговых детекторов/Взаимные калибровки/Меньше шаг по мощности/m4.1t35s900O.txt', 'float64')
q_PMT = np.genfromtxt('C:/Users/Пользователь/Desktop/Лаба/Калибровки/405/Продолжение работы по калибровки аналоговых детекторов/Взаимные калибровки/Меньше шаг по мощности/m4.1t35s900F.txt', 'float64')
for k in range(1200, 10000, 10):
    # q_APD_1 = np.array([], 'float64')
    # q_PMT_1 = np.array([], 'float64')

    with open('C:/Users/Пользователь/Desktop/3.txt', "w+") as file:
        for i in range(q_APD.size):
            if q_APD[i] > k:
                # q_PMT_1 = np.append(q_PMT_1, q_PMT[i])
                file.write(str(q_PMT[i])+'\n')
            else:
                file.write('0'+'\n')

        my_file1 = "C:/Users/Пользователь/Desktop/Лаба/Калибровки/405/Продолжение работы по калибровки аналоговых детекторов/Взаимные калибровки/Меньше шаг по мощности/m4.1t35s900O.txt"
        # my_file2 = "C:/Users/Пользователь/Desktop/Лаба/Калибровки/405/Со СЧЕТНЫМ ФЭУ/Экспериенты со счетным ФЭУ/FN в сигнальном канале/2 ФЭУ строб 500нс 5 min (gain 550 and 852)/m31(0.7)s500d100FO.txt"

        my_file2 = "C:/Users/Пользователь/Desktop/3.txt"

        file_name = "C:/Users/Пользователь/Desktop/file_name.txt"

    fileVar = open(file_name, "a+")
    fileVar.close()

    # j = 0
    # for j in range(0, 1, 1):

    X = delete_noize_new(my_file1, 2016, 99999, 0, 0, 0, 0, 'new_file1.txt')
    Y = delete_noize_new(my_file2, 0, 99999, 0, 0, 0, 0, 'new_file2.txt')
    g = G(X, Y, 4630, 3841, 0.22841, 0)
    # print(j, g)
    print(k, g)
