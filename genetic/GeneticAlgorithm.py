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
    # logging.info("Pairs size: %d", len(pairs))
    # logging.info("=========== PARENTS AFTER PARING ============ ")
    # for i in range(len(parents)):
    #     logging.info("PSL ======================= %d", fitness_function(parents[i]))
    # logging.info("=========== THE END ============ ")
    return pairs


# Скрещивание родителей
def crossover(population):
    parents = make_pairs(population)
    # logging.info("=========== POPULATION BEFORE CROSSOVER ============ ")
    # for i in range(len(population)):
    #     logging.info("PSL ======================= %d", fitness_function(population[i]))
    # logging.info("=========== THE END ============ ")
    #
    # logging.info("=========== PAIRS BEFORE CROSSOVER ============ ")
    # for i in range(len(parents)):
    #     logging.info("PSL ======================= %d", fitness_function(parents[i][0]))
    #     logging.info("PSL ======================= %d", fitness_function(parents[i][1]))
    # logging.info("=========== THE END ============ ")
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

    # logging.info("=========== POPULATION AFTER CROSSOVER ============ ")
    # for i in range(len(population)):
    #     logging.info("PSL ======================= %d", fitness_function(population[i]))
    # logging.info("=========== THE END ============ ")
    #
    # logging.info("=========== PAIRS AFTER CROSSOVER ============ ")
    # for i in range(len(parents)):
    #     logging.info("PSL ======================= %d", fitness_function(parents[i][0]))
    #     logging.info("PSL ======================= %d", fitness_function(parents[i][1]))
    # logging.info("=========== THE END ============ ")
    return children_list


# Мутация детей
def mutate(children_array):
    for i in range(len(children_array)):
        if random() < Pm:
            index = randint(0, N - 1)
            temp_child = children_array[i][:]
            children_array[i][index] = -temp_child[index]
            logging.info("Child with id %d and index %d was %d and now it's %d", i, index, -temp_child[index], temp_child[index])
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
        logging.info("PSL ======================= [%d] %d", i, N/fitness_function(population[i]))
    logging.info("=========== THE END ============ ")
    while len(next_population) < P:
        best_id = -1
        best_fx = -100
        for i in range(len(population)):
            # Получение значения функции приспособленности
            # для текущей особи в популяции
            ffx = fitness_function(population[i])
            ffx_psl = N/ffx
            # Находим наиболее приспособленную особь
            if ffx > best_fx:
                best_id = i
                best_fx = ffx
                # Если эта особь имеет подходящий нам БЛ:
                # добавляем в список лучших
            # temp
            if all_best_psl > ffx_psl:
                all_best_psl = ffx_psl
            # Массив значений функции приспособленности текущей популяции
            # для отрисовки графика
        best_psl = N/best_fx
        if best_psl <= PSL_MAX:
            best_of_the_best.append(population[best_id][:])
        next_population.append(population.pop(best_id))
        fitness_array.append(best_fx)

    logging.info("=========== NEXT POPULATION ============ ")
    for i in range(len(next_population)):
        logging.info("PSL ======================= %d", N/fitness_function(next_population[i]))
    logging.info("=========== THE END ============ ")
    # for i in range(len(psl_array)):
    #     s
    return [best_of_the_best, next_population, sum(fitness_array)/len(fitness_array), best_id, all_best_psl]


def fitness_function(element):
    function_info = function(element)
    return N/function_info[1]


def trim_array(array_for_trimming):
    trimmed_array = list()
    for i in range(len(array_for_trimming)):
        if not trimmed_array.__contains__(array_for_trimming[i]):
            trimmed_array.append(array_for_trimming[i])
    return trimmed_array


if __name__ == '__main__':
    population_number = 0
    current_population = generate_population()
    best_of_the_best_array = dict()
    best_array = list()
    best_r_array = list()
    average_psl_array = list()
    isFinished = False
    while not isFinished:
        population_number = population_number + 1
        # logging.info("=========== CURRENT POPULATION BEFORE CHILDREN ============ ")
        # for i in range(len(current_population)):
        #     logging.info("PSL ======================= [%d]: %d", i, fitness_function(current_population[i]))
        # logging.info("=========== THE END ============ ")

        children = crossover(current_population)

        #
        # logging.info("=========== CHILDREN BEFORE MUTATION ============ ")
        # for i in range(len(children)):
        #     logging.info("PSL ======================= [%d]: %d", i, fitness_function(children[i]))
        # logging.info("=========== THE END ============ ")

        # mutated_children = mutate(children)

        # logging.info("=========== MUTATED CHILDREN ============ ")
        # for i in range(len(mutated_children)):
        #     logging.info("PSL ======================= [%d]: %d", i, fitness_function(mutated_children[i]))
        # logging.info("=========== THE END ============ ")
        current_population.extend(mutate(children))

        # logging.info("=========== CURRENT POPULATION AFTER MUTATION ============ ")
        # for i in range(len(current_population)):
        #     logging.info("PSL ======================= [%d]: %d", i, fitness_function(current_population[i]))
        # logging.info("=========== THE END ============ ")

        tournament_result = tournament(current_population)
        # logging.info("=========== CURRENT POPULATION BEFORE MUTATION ============ ")
        # for i in range(len(current_population)):
        #     logging.info("PSL ======================= [%d]: %d", i, N/fitness_function(current_population[i]))
        # logging.info("=========== THE END ============ ")

        best_of_the_best_array = tournament_result[0]
        logging.info("Current best arrays size ======================= %d", len(best_of_the_best_array))
        logging.info("Current best PSL ======================= %d", tournament_result[4])
        if len(best_of_the_best_array) >= K:
            best_array = current_population[tournament_result[3]]
            isFinished = True
        current_population = tournament_result[1]
        average_psl_array.append(tournament_result[2])
        # plot
        logging.info("Population number: %d", population_number)
        logging.info("Average PSL: %d", tournament_result[2])

    x = list()
    for k in range(population_number):
        x.append(k)
    plt.plot(x, average_psl_array)
    plt.show()

    temp_best_r_array = function(best_array)[2]
    best_r_array = temp_best_r_array[:]
    for i in range(len(temp_best_r_array) - 2, -1, -1):
        best_r_array.append(temp_best_r_array[i])

    x = list()
    for i in range(-N + 1, N):
        x.append(i)
    plt.plot(x, best_r_array)
    plt.show()
    # test_array = [-1, 1, -1, -1, 1, 1, 1]
    # function(test_array)
    # gen_array = generate_population()
    # print(len(gen_array))
    # pair_array = make_pairs(gen_array)
    # print(len(pair_array))
