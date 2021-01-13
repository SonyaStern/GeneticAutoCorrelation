import logging
import matplotlib.pyplot as plt
from random import random, randint

N = 37
P = 70
PSL_MAX = 3
K = 3
Pk = 0.9
Pm = 0.1
logging.basicConfig(level=logging.INFO)


# Получение результата функции
def function(array):
    psl = -100
    R = 0
    # массив значений R
    R_array = list()
    for k in range(-N + 1, 1):
        R = 0
        for i in range(N + k):
            R += array[i] * array[i - k]
        R_array.append(R)
        # Получение значения максимального БЛ
        if psl < R != N:
            psl = R
    # Обдумать возвращаемые аргументы
    return [R, psl, R_array]


# Создание первой популяции из рандомных элементов
def generate_population():
    population = list()
    while len(population) < P:
        # Массив значений одной особи
        temp_array = []
        for j in range(N):
            temp = random()
            if temp < 0.5:
                temp_array.append(-1)
            else:
                temp_array.append(1)
        # Проверка на уникальность
        if not population.__contains__(temp_array):
            population.append(temp_array)
    logging.info("Generation size: %d", len(population))
    return population


# Создание пар родителей
def make_pairs(parents):
    pairs = list()
    temp_parents = parents.copy()
    while len(temp_parents) > 0:
        randomizer = randint(0, len(temp_parents) - 1)
        first_parent = temp_parents.pop(randomizer)
        randomizer = randint(0, len(temp_parents) - 1)
        second_parent = temp_parents.pop(randomizer)
        b = random()
        if b < Pk:
            pairs.append([first_parent, second_parent])
    return pairs


# Скрещивание родителей
def crossover(population):
    parents = make_pairs(population)
    children_list = list()
    for i in range(len(parents)):
        first_child = parents[i][0][:]
        second_child = parents[i][1][:]
        randomizer = randint(0, N - 1)
        for j in range(randomizer, N):
            first_child[j] = parents[i][1][j]
            second_child[j] = parents[i][0][j]
        children_list.append(first_child)
        children_list.append(second_child)
    logging.info("Children size: %d", len(children_list))
    return children_list


# Мутация детей
def mutate(children_array):
    for i in range(len(children_array)):
        if random() < Pm:
            index = randint(0, N - 1)
            temp_child = children_array[i][:]
            children_array[i][index] = -temp_child[index]
            logging.info("Child with id %d and index %d was %d and now it's %d", i, index, -temp_child[index],
                         temp_child[index])
    return children_array


# Отбор лучших детей и родителей в следующее поколение методом турнира
def tournament(population):
    population = trim_array(population)
    next_population = list()
    best_of_the_best = list()
    fitness_array = list()
    # temp
    all_best_psl = 100
    best_id = 0
    logging.info("=========== CURRENT POPULATION BEFORE TOURNAMENT ============ ")
    for i in range(len(population)):
        logging.info("PSL ======================= [%d] %d", i, N / fitness_function(population[i]))
    logging.info("=========== THE END ============ ")
    while len(next_population) < P:
        best_id = -1
        best_fx = -100
        for i in range(len(population)):
            # Получение значения функции приспособленности
            # для текущей особи в популяции
            ffx = fitness_function(population[i])
            ffx_psl = N / ffx
            # Находим наиболее приспособленную особь
            if ffx > best_fx:
                best_id = i
                best_fx = ffx
            # temp
            if all_best_psl > ffx_psl:
                all_best_psl = ffx_psl
            # Массив значений функции приспособленности текущей популяции
            # для отрисовки графика
        best_psl = N / best_fx
        # Если эта особь имеет подходящий нам БЛ:
        # добавляем в список лучших
        if best_psl <= PSL_MAX:
            best_of_the_best.append(population[best_id][:])
        next_population.append(population.pop(best_id))
        fitness_array.append(best_fx)
    return [best_of_the_best, next_population, sum(fitness_array) / len(fitness_array), best_id, all_best_psl]


# Получение значения функции приспособленности
def fitness_function(element):
    function_info = function(element)
    return N / function_info[1]


# Удаление повторяющихся особей
def trim_array(array_for_trimming):
    trimmed_array = list()
    for i in range(len(array_for_trimming)):
        if not trimmed_array.__contains__(array_for_trimming[i]):
            trimmed_array.append(array_for_trimming[i])
    return trimmed_array


def create_report(reported_population):
    print("Номер особи |  КП                                                                                                                                  | Значение PSL")
    for i in range(len(reported_population)):
        print(i, "          | ", reported_population[i], " | ", function(reported_population[i])[1])


if __name__ == '__main__':
    population_number = 0
    current_population = generate_population()
    best_of_the_best_array = dict()
    best_array = list()
    best_r_array = list()
    average_psl_array = list()
    isFinished = False

    # Информация для отчёта
    first_population = list()
    third_population = list()
    last_population = list()
    while not isFinished:
        population_number = population_number + 1
        children = crossover(current_population)
        current_population.extend(mutate(children))
        tournament_result = tournament(current_population)

        best_of_the_best_array = tournament_result[0][:]
        current_population = tournament_result[1][:]
        logging.info("Current best arrays size ======================= %d", len(best_of_the_best_array))
        logging.info("Current best PSL ======================= %d", tournament_result[4])

        if population_number == 1:
            first_population = current_population[:]
        if population_number == 3:
            third_population = current_population[:]
        if len(best_of_the_best_array) >= K:
            best_array = current_population[tournament_result[3]][:]
            last_population = current_population[:]
            isFinished = True
        average_psl_array.append(tournament_result[2])
        logging.info("Population number: %d", population_number)
        logging.info("Average PSL: %d", tournament_result[2])

    # Отрисовка графика зависимости
    # значения PSL от номера популяции
    x = list()
    for k in range(population_number):
        x.append(k)
    plt.plot(x, average_psl_array)
    plt.show()

    # Отрисовка графика АКФ
    # для лучшей особи в популяции
    temp_best_r_array = function(best_array)[2]
    best_r_array = temp_best_r_array[:]
    for i in range(len(temp_best_r_array) - 2, -1, -1):
        best_r_array.append(temp_best_r_array[i])
    x = list()
    for i in range(-N + 1, N):
        x.append(i)
    plt.plot(x, best_r_array)
    plt.show()

    # Создание отчёетов
    print("Первая популяция")
    create_report(first_population)
    print("Третья популяция")
    create_report(third_population)
    print("Последняя популяция")
    create_report(last_population)