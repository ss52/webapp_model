# %%
# TODO:
# 1.
# 2.
#

import math
import json


def export_json_file(time, w):
    """
    Экспортируем данные модели в файл json:
    w - степень окисления, %
    time - время, мин
    """

    data = {
        "w": w,
        "time": time
    }

    with open('export.json', 'w') as f:
        json.dump(data, f)


def import_json_file(file_name):
    """
    Из файла исходных данных json получаем словарь
    """

    with open(file_name) as json_file:
        data = json.load(json_file)

    return data


def batch_calc(input_data):
    """
    Модель расчета окисления материала в периодическом режиме на основе КФ.

    На вход подается словарь.
    Описание параметров и тестовые значения:
    m = 0.1137  # масса материала, кг
    V = 0.72  # объем жидкой фазы, л
    U0 = 1  # U0, мольО2 / (л * ч * атм)
    PO2 = 7  # Парциальное давление кислорода, бар
    T = 200 + 273.16  # Темпераутра, К
    dt1 = 1  # Шаг по времени, мин
    tt = 20  # Продолжительность процесса, мин
    Acid0 = 0  # Начальная концентрация кислоты, г/л
    kappa = 0.5  # Каппа
    s = 1  # Доля компонента
    T0 = 210 + 273.16  # Стандартная температура, К
    betaO = 11.25  # Стехиометрический расход кислорода, моль/кг
    alfaO = 0.62  # Порядок реакции по кислороду
    betaA = 0  # Расход кислоты, кг/кг
    alfaA = 0  # Порядок реакции по кислоте
    tau0 = 0.59  # Время полного растворения, ч
    EdR = 6323  # E/R
    a = -2.18  # Коэф. КФ
    b = 5.9  # Коэф. КФ
    c = -10.3  # Коэф. КФ
    d = 6.2  # Коэф. КФ
    vd = 0  # Воднорастворимая доля
    psr = 1  # Предельная степень окисления

    Возвращаемые значения:
    time - время, мин
    w - степень окисления, %
    """
    def KU0(delta, T):
        T = (T - 273) / 100
        if T > 2.5:
            T = 2.5
        if T < 0.2:
            T = 0.2
        x = 2.24296 * T * T * T - 4.07952 * T * T + 6.72472 * T - 0.49254
        # x2 = 0.7846 * math.exp(1.39 * T)
        x3 = 0.1212 * math.log(delta) + 0.5375

        return x * x3

    def myPower(aa, x):
        if x == 0:
            return 1
        elif aa == 0:
            return 0
        else:
            return math.exp(x * math.log(aa))

    def deriv(x):
        """
        Производная КФ в точке x
        """
        if x < 1:
            der = (1 - x) * (a + 2 * b * x + 3 * c * x ** 2 + 4 * d * x ** 3) \
                - (1 + a * x + b * x ** 2 + c * x ** 3 + d * x ** 4)
        else:
            der = 0

        if der > 0:
            der = 0

        return der

    def iter0(pe):
        a1 = k01 * myPower(Acid, alfaA) * myPower(kappa * pe, alfaO) * deriv(x1)
        pe1 = PO2 - a1
        return pe - pe1

    def iters(pe):
        x1 = x01 + kk1 * (myPower(kappa * pe0, alfaO) + myPower(kappa * pe, alfaO))

        if x1 > 1:
            x1 = 1

        a1 = k1 * myPower(kappa * pe, alfaO) * deriv(x1)

        pe1 = PO2 - a1
        return pe - pe1

    def bisect(min, max, eps, itermax, func):
        iter = 0

        while iter < itermax:
            sred = (min + max) / 2

            fsred = func(sred)
            fmin = func(min)
            fmax = func(max)

            if fmin * fmax > 0:
                return sred

            if abs(fsred) < eps:
                return sred

            if fmin * fsred < 0:
                min = min
                max = sred
            else:
                min = sred
                max = max

            iter += 1
        else:
            return sred

    def omega(x):
        omega = (1 - x) * (1 + a * x + b * x ** 2 + c * x ** 3 + d * x ** 4)
        if omega < 0:
            omega = 0

        return omega

    m = input_data['m']
    V = input_data['V']
    U0 = input_data['U0']
    PO2 = input_data['PO2']
    T = input_data['T'] + 273.16
    dt1 = input_data['dt1']
    tt = input_data['tt']
    Acid0 = input_data['Acid0']
    kappa = input_data['kappa']
    s = input_data['s']
    T0 = input_data['T0'] + 273.16
    betaO = input_data['betaO']
    alfaO = input_data['alfaO']
    betaA = input_data['betaA']
    alfaA = input_data['alfaA']
    tau0 = input_data['tau0']
    EdR = input_data['EdR']
    a = input_data['a']
    b = input_data['b']
    c = input_data['c']
    d = input_data['d']
    vd = input_data['vd']
    psr = input_data['psr']

    dt = 0.1 / 300
    te = 0
    x1 = 0
    x01 = 0

    nnn = round(dt1 / 60 / dt)
    nn = nnn - 1

    delta = V / m
    U0 = U0 * KU0(delta, T)
    m1 = m * s * (psr - vd)
    k01 = -betaO * m1 / V / U0 / tau0 * math.exp(-EdR * (1 / T - 1 / T0))
    kk01 = math.exp(-EdR * (1 / T - 1 / T0)) * dt / 2 / tau0

    Acid = Acid0

    pe1 = bisect(0, PO2, 0.00001, 100, iter0)
    pe0 = pe1

    nn = 0

    Acid1 = Acid0
    w = []  # степень окисления
    time = []  # время опыта
    pe = []  # эквивалентное давление
    w_prev = 0  # значение степени окисления за прошлую минуту

    while (te * 60) < (tt + 0.1):
        te = te + dt

        k1 = k01 * myPower(Acid1, alfaA)
        kk1 = kk01 * myPower(Acid1, alfaA)

        pe1 = bisect(0, PO2, 0.00001, 100, iters)
        x1 = x01 + kk1 * (myPower(kappa * pe0, alfaO) + myPower(kappa * pe1, alfaO))

        nn += 1

        if nn == nnn:
            w1 = (psr - vd) * (1 - omega(x1)) + vd
            if w1 * 100 >= w_prev:
                w.append(round(w1 * 100, 1))
                w_prev = w1 * 100
            else:
                w.append(round(w_prev, 1))
            pe.append(round(pe1 * kappa, 2))
            time.append(round(te * 60, 0))
            nn = 0

        x01 = x1
        pe0 = pe1

    return time, w
