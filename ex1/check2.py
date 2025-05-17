import time
import ex1
import search
GREEN = '\033[92m'  # Green text
RED = '\033[91m'    # Red text
RESET = '\033[0m'   # Reset to default color

def run_problem(func, targs=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)
    except Exception as e:
        result = (-3, e)
    return result

def solve_problems(problem, algorithm, supposedLen, total_time):
    print("Problem:")
    for row in problem:
        print(row)

    try:
        p = ex1.create_zuma_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return total_time

    start_time = time.time()  # Start the timer
    if algorithm == "gbfs":
        result = run_problem((lambda p: search.greedy_best_first_graph_search(p, p.h)), targs=[p])
    else:  # Default to A*
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])
    end_time = time.time()  # End the timer

    elapsed_time = end_time - start_time
    total_time += elapsed_time

    print(f"Time it took {algorithm} = {elapsed_time:.6f} secs.")
    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        print("len:", len(solution), "best len:", supposedLen, solution)
        if (len(solution) == supposedLen):
            print(f"{GREEN}###############GOOD LENGTH###############{RESET}")
        else:
            print(f"{RED}@@@@@@@@@@@@@@@@PATH TOO SHORT@@@@@@@@@@@@@@@@{RESET}")
    else:
        if (supposedLen == "no"):
            print("no solution,", "supposed to be:", supposedLen)
            print(f"{GREEN}###############GOOD LENGTH###############{RESET}")
        else:
            print(f"{RED}@@@@@@@@@@@@@@@@DIDNT FIND PATH@@@@@@@@@@@@@@@@{RESET}")

    return total_time

problem1 = ((1, 1), (1,))  # 1, t: 0
problem2 = ((1, 2, 2, 1, 1), (2, 1))  # 1, t: 0
problem3 = ((1, 2, 3, 3, 2, 2, 1, 1), (3,))  # 1, t: 0
problem4 = ((2, 2, 3, 2), (3, 3))  # 2, t: 0
problem5 = ((2, 2, 3, 2), (3, 3, 2, 1, 2, 2, 4))  # 2, t: 0
problem6 = ((2, 2, 3, 3, 2), (1, 3))  # 2, t: 0
problem7 = ((3, 3, 4, 4, 3, 3), (3, 4))  # 2, t: 0
problem8 = ((1, 1, 2, 2, 1, 1, 3, 3, 4, 4, 3, 1, 1), (2, 4, 3, 3, 3, 1))  # 2, t: 0
problem9 = ((2, 3, 3, 2), (1, 2, 3))  # 3, t: 0
problem10 = ((4, 1, 2, 3, 3, 2, 2, 1, 1), (4, 3, 4))  # 3, t: 0
problem11 = ((1, 1, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 4, 1, 1, 4, 3, 3, 2, 2, 3, 3, 1, 1), (3, 4, 1, 2, 3, 4))  # 3, t: 0
problem12 = ((2, 2, 3, 3, 1), (1, 1, 2, 3))  # 4, t: 0
problem13 = ((4, 2, 2, 3, 3, 2), (1, 3, 4, 4))  # 4, t: 0
problem14 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4))  # 4, t: 0
problem15 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))  # 4, t: 0
problem16 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 1, 2))  # 4, t: 0.05, 0
problem17 = ((1, 1, 3, 3, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 3, 3, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))  # 4, t: 0.1, 0
problem18 = ((2, 2, 3, 3, 1), (4, 1, 1, 2, 3))  # 5, t: 0
problem18_1 = ((1, 2, 2, 1, 1, 3, 3, 1), (4, 2, 3, 4, 4, 2, 1))  # 5, t: 0
problem19 = ((1, 2, 2, 1, 1, 3, 3, 1), (4, 2, 3, 4, 4, 3, 2, 3, 2, 2, 3, 1, 1))  # 5, t: 0
problem20 = ((1, 1, 2, 4, 1, 1, 4, 3, 3, 2, 2, 3, 3, 1, 1), (3, 4, 1, 2, 3, 4))  # 5, t: 0.25, 0.1
problem21 = ((1, 1, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 2, 3, 4))  # 5, t: 0.21, 0.05
problem22 = ((1, 1, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 1, 3))  # 5, t: 0.17, 0.03
problem22_1 = ((1, 1, 3, 3, 2, 2, 3, 1, 2, 3, 3, 2, 2, 3, 3, 1, 1), (3, 1, 2, 4, 3, 4, 3, 1))  # 5, t: 0.08, 0.03
problem22_2 = ((1, 1, 3, 3, 2, 2, 3, 1, 4, 2, 3, 3, 2, 2, 3, 3, 1, 1), (3, 4, 1, 2, 4, 3, 4, 3, 1))  # 6, t: 9.6, 2
problem23 = ((3, 3, 4, 4, 3, 3), (3, 1, 2, 3, 2, 1, 4))  # 7, t: 0
problem24 = ((1, 3, 3, 2, 1, 2, 2), (1, 3, 2, 4, 2, 3, 2))  # 7, t: 0
problem25 = ((3, 3, 1, 4, 2, 4, 4, 1, 2, 4, 3), (2, 2, 2, 2, 4, 4, 1, 3))  # 7, t: 0.06
problem25_1 = ((1, 1, 2, 2, 1, 1, 3, 3, 4, 4, 3, 1, 1), (3, 3, 3, 3, 3, 2, 4, 3, 3, 3, 1))  # 7, t: 0.23, 0.06
problem25_2 = ((3, 3, 1, 1, 4, 3, 2, 4, 3, 3, 2, 4, 4, 1, 3), (4, 4, 2, 2, 3, 3, 3, 1, 3))  # 7, t: 9.6, 7.2
problem26 = ((1, 3, 3, 2, 1, 2, 2), (1, 3, 2, 4, 2, 3, 4, 2))  # 8, t: 0.03, 0.01
problem27 = ((1, 2, 1, 2), (1, 2, 4, 1, 2, 2, 4, 1, 3, 2, 1, 2))  # 10, t: 0
problem28 = ((2, 2, 3, 2), (3, 1))  # no, t: 0
problem29 = ((4, 2, 2, 3, 3, 2), (1, 3))  # no, t: 0
problem30 = ((2, 2, 3, 3, 2, 4), (2, 2, 3, 2))  # no, t: 0
problem31 = ((4, 2, 2, 3, 3, 2), (1, 3, 4))  # no, t: 0
problem32 = ((4, 2, 2, 3, 3, 1), (1, 1, 2, 3))  # no, t: 0

p1 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))

# p2 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))

# p3 = ((3, 3, 1, 4, 2, 4, 4, 1, 2, 4, 3), (2, 2, 2, 2, 4, 4, 1, 3))

p4 = ((3, 3, 1, 4, 2, 4, 4, 1, 2, 4, 3), (2, 2, 2, 2, 4, 4, 1, 3))


total_time = 0

# Define all test problems
problems = [
    # (problem1, 1),
    # (problem2, 1),
    # (problem3, 1),
    # (problem4, 2),
    # (problem5, 2),
    # (problem6, 2),
    # (problem7, 2),
    # (problem8, 2),
    # (problem9, 3),
    # (problem10, 3),
    # (problem11, 3),
    # (problem12, 4),
    # (problem13, 4),
    # (problem14, 4),
    # (problem15, 4),
    # (problem16, 4),
    # (problem17, 4),
    # (problem18, 5),
    # (problem19, 5),
    # (problem20, 5),
    # (problem21, 5),
    # (problem22, 5),
    # # (problem22_1, 5),
    # # (problem22_1, 5),
    # # (problem22_2, 6),
    # (problem23, 7),
    # (problem24, 7),
    # (problem25, 7),
    # (problem26, 8),
    # (problem27, 10),
    # (problem28, "no"),
    # (problem29, "no"),
    # (problem30, "no"),
    # (problem31, "no"),
    # (problem32, "no"),
    (p1, 4),
    (p4, 7)
]

# Test all problems with both algorithms
i = 0
algos= ["gbfs", "astar"] #
for problem, expected_len in problems:
    for algo in algos: # "astar" or "gbfs"
        print(f"###################### iteration {i} out of {len(problems)* len(algos)} ######################")
        i += 1
        total_time = solve_problems(problem, algo, expected_len, total_time)
        print("total time:", total_time)
print(f"Total time for all problems: {total_time:.6f} secs.")
