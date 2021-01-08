import logging
import matplotlib.pyplot as plt
from random import random, randint

N = 37
P = 10
PSL_MAX = 3
K = 3
Pk = 0.9
Pm = 0.1
logging.basicConfig(level=logging.INFO)


# Получение результата функции в зависимости от a,k
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
            # if not population.__contains__(temp_array):
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
            pairs.append(Pair(first_parent, second_parent))
    logging.info("Pairs size: %d", len(pairs))
    logging.info("=========== PARENTS AFTER PARING ============ ")
    for i in range(len(parents)):
        logging.info("PSL ======================= %d", fitness_function(parents[i]))
    logging.info("=========== THE END ============ ")
    return pairs


# Скрещивание родителей
def crossover(population):
    parents = make_pairs(population)
    logging.info("=========== POPULATION BEFORE CROSSOVER ============ ")
    for i in range(len(population)):
        logging.info("PSL ======================= %d", fitness_function(population[i]))
    logging.info("=========== THE END ============ ")

    logging.info("=========== PAIRS BEFORE CROSSOVER ============ ")
    for i in range(len(parents)):
        logging.info("PSL ======================= %d", fitness_function(parents[i].first_parent))
        logging.info("PSL ======================= %d", fitness_function(parents[i].second_parent))
    logging.info("=========== THE END ============ ")
    # TODO: FIX IT
    children_list = list()
    for i in range(len(parents)):
        first_child = parents[i].first_parent
        second_child = parents[i].second_parent
        randomizer = randint(0, N - 1)
        for j in range(randomizer, N):
            first_child[j] = parents[i].second_parent[j]
            second_child[j] = parents[i].first_parent[j]
        children_list.append(first_child)
        children_list.append(second_child)
    logging.info("Children size: %d", len(children_list))

    logging.info("=========== POPULATION AFTER CROSSOVER ============ ")
    for i in range(len(population)):
        logging.info("PSL ======================= %d", fitness_function(population[i]))
    logging.info("=========== THE END ============ ")
    return children_list


# Мутация детей
def mutate(children_array):
    for i in range(len(children_array)):
        if random() < Pm:
            index = randint(0, N - 1)
            children_array[i][index] = -children_array[i][index]
            logging.info("Child with index %d and element %d was %d and now it's %d", i, index, -children_array[i][index], children_array[i][index])
    return children_array


# Отбор лучших детей и родителей в следующее поколение методом турнира
def tournament(population):
    next_population = list()
    best_of_the_best = dict()
    all_best_psl = 100
    logging.info("=========== CURRENT POPULATION ============ ")
    for i in range(len(population)):
        logging.info("PSL ======================= %d", fitness_function(population[i]))
    logging.info("=========== THE END ============ ")
    while len(next_population) < P:
        best_id = -1
        best_psl = 100
        for i in range(len(population)):
            # Получение максимального БЛ для текущей особо в популяции
            fx_psl = fitness_function(population[i])
            # Если эта особь имеет БЛ лучше, чем у предыдущей:
            # добавляем в следующее поколение
            if 0 < fx_psl < best_psl:
                best_id = i
                best_psl = fx_psl
                # temp
                if all_best_psl > best_psl:
                    all_best_psl = best_psl
                # Если эта особь имеет подходящий нам БЛ:
                # добавляем в список лучших
                if fx_psl <= PSL_MAX:
                    best_of_the_best.update({i: population[i]})
        next_population.append(population.pop(best_id))
    logging.info("=========== NEXT POPULATION ============ ")
    for i in range(len(next_population)):
        logging.info("PSL ======================= %d", fitness_function(next_population[i]))
    logging.info("=========== THE END ============ ")
    return [best_of_the_best, next_population, all_best_psl]


def fitness_function(element):
    function_info = function(element)
    return function_info[1]


# Класс для формирования пар родителей
class Pair:
    def __init__(self, first_parent, second_parent):
        self.first_parent = first_parent
        self.second_parent = second_parent


if __name__ == '__main__':
    population_number = 0
    current_population = generate_population()
    best_array = dict()
    isFinished = False
    while not isFinished:
        population_number = population_number + 1
        logging.info("=========== CURRENT POPULATION BEFORE CHILDREN ============ ")
        for i in range(len(current_population)):
            logging.info("PSL ======================= [%d]: %d", i, fitness_function(current_population[i]))
        logging.info("=========== THE END ============ ")

        children = crossover(current_population)

        logging.info("=========== CURRENT POPULATION BEFORE MUTATION ============ ")
        for i in range(len(current_population)):
            logging.info("PSL ======================= [%d]: %d", i, fitness_function(current_population[i]))
        logging.info("=========== THE END ============ ")

        logging.info("=========== CHILDREN BEFORE MUTATION ============ ")
        for i in range(len(children)):
            logging.info("PSL ======================= [%d]: %d", i, fitness_function(children[i]))
        logging.info("=========== THE END ============ ")

        mutated_children = mutate(children)

        logging.info("=========== MUTATED CHILDREN ============ ")
        for i in range(len(mutated_children)):
            logging.info("PSL ======================= [%d]: %d", i, fitness_function(mutated_children[i]))
        logging.info("=========== THE END ============ ")
        current_population.extend(mutated_children)

        logging.info("=========== CURRENT POPULATION AFTER MUTATION ============ ")
        for i in range(len(current_population)):
            logging.info("PSL ======================= [%d]: %d", i, fitness_function(current_population[i]))
        logging.info("=========== THE END ============ ")

        tournament_result = tournament(current_population)
        best_array = tournament_result[0]
        logging.info("Current best arrays size ======================= %d", len(best_array))
        logging.info("Current best PSL ======================= %d", tournament_result[2])
        if len(best_array) >= K:
            isFinished = True
        current_population = tournament_result[1]
        # plot
        logging.info("Population number: %d", population_number)

    x = list()
    for k in range(-K, 1):
        x.append(k)
    # y = function(current_population[best_array])[2]
    # plt.plot(x, function(current_population[best_array]))
    # plt.show()
    # test_array = [-1, 1, -1, -1, 1, 1, 1]
    # function(test_array)
    # gen_array = generate_population()
    # print(len(gen_array))
    # pair_array = make_pairs(gen_array)
    # print(len(pair_array))
