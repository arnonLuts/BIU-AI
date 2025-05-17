import ex1
import search


def run_problem(func, targs=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)


    except Exception as e:
        result = (-3, e)


    return result


# check_problem: problem, search_method, timeout
# timeout_exec: search_method, targs=[problem], timeout_duration=timeout
def solve_problems(problem, algorithm):
    for row in problem:
        print(row)

    try:
        p = ex1.create_zuma_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return None

    if algorithm == "gbfs":
        result = run_problem((lambda p: search.greedy_best_first_graph_search(p, p.h)),targs=[p])
    else:
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])

    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        print(len(solution), solution)
    else:
        print("no solution")


problem1 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))
# solution1: len(solution) = 4
problem2 = ((3, 3, 1, 4, 2, 4, 4, 1, 2, 4, 3), (2, 2, 2, 2, 4, 4, 1, 3))
# solution2: len(solution) = 7

problem4 = ((1, 2, 2, 1, 1, 3, 4, 3, 3, 1, 2, 2, 3, 3, 4, 4, 1), (3, 2, 2, 1, 1, 3, 3, 3))
problem5 = ((1, 1, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2), (4, 1, 3, 1, 3, 3))
problem19 = ((1, 2, 2, 1, 1, 3, 3, 1), (4, 2, 3, 4, 4, 3, 2, 3, 2, 2, 3, 1, 1))  # 5, t: 0.09
problem22 = ((1, 1, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 1, 2, 3, 4))  # 5, t: 3.17
problem2222 = ((1, 1, 3, 1, 4, 4, 1), (2, 3, 3, 4, 2, 2, 2, 2))
problema = ((1,1 ), (2, 2))
pr = ((1,2,2,1),(2,1))
def main():
    problem = pr
    algorithm = "gbfs"  # or "astar"

    solve_problems(problem, algorithm)


if __name__ == '__main__':
    main()
