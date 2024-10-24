from multiprocessing import Pool
import time

# Функции для формул
def formula_1(x):
    return x**2 - x**2 + x*4 - x*5 + x + x

def formula_2(x):
    return x + x

# Функция для вычисления суммы (формула 3)
def formula_3(result1, result2):
    return result1 + result2

# Функция для выполнения вычислений в процессе
def compute_in_process(iterations):
    with Pool() as pool:
        # Выполняем вычисления по формуле 1
        start_formula_1 = time.time()
        results1 = pool.map(formula_1, range(iterations))
        end_formula_1 = time.time()

        # Выполняем вычисления по формуле 2
        start_formula_2 = time.time()
        results2 = pool.map(formula_2, range(iterations))
        end_formula_2 = time.time()

        # Вычисление итоговой суммы (формула 3)
        start_formula_3 = time.time()
        final_results = [formula_3(r1, r2) for r1, r2 in zip(results1, results2)]
        end_formula_3 = time.time()

    formula_1_time = end_formula_1 - start_formula_1
    formula_2_time = end_formula_2 - start_formula_2
    formula_3_time = end_formula_3 - start_formula_3
    total_time = (end_formula_1 - start_formula_1) + (end_formula_2 - start_formula_2) + (
                end_formula_3 - start_formula_3)

    print(f"Время формулы 1: {formula_1_time}")
    print(f"Время формулы 2: {formula_2_time}")
    print(f"Время формулы 3: {formula_3_time}")
    print(f"Общее время: {total_time}")
    print("-" * 40)


if __name__ == '__main__':
    # Выполнение для 10,000 и 100,000 итераций с процессами
    compute_in_process(10000)
    compute_in_process(100000)