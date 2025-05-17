import time
import ex1
from ex1_check import solve_problems

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
problem14 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4))  # 4, t: 0.09
problem15 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))  # 4, t: 0.09
problem16 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 1, 2, 3, 4))  # 4, t: 0.18
problem17 = ((1, 1, 3, 3, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 3, 3, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))  # 4, t: 0.32
problem18 = ((2, 2, 3, 3, 1), (4, 1, 1, 2, 3))  # 5, t: 0
problem19 = ((1, 2, 2, 1, 1, 3, 3, 1), (4, 2, 3, 4, 4, 3, 2, 3, 2, 2, 3, 1, 1))  # 5, t: 0.09
problem20 = ((1, 1, 2, 4, 1, 1, 4, 3, 3, 2, 2, 3, 3, 1, 1), (3, 4, 1, 2, 3, 4))  # 5, t: 6.1
problem21 = ((1, 1, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 2, 3, 4))  # 5, t: 3.12
problem22 = ((1, 1, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 1, 2, 3, 4))  # 5, t: 3.17
problem23 = ((3, 3, 4, 4, 3, 3), (3, 1, 2, 3, 2, 1, 4))  # 7, t: 0
problem24 = ((1, 3, 3, 2, 1, 2, 2), (1, 3, 2, 4, 2, 3, 2))  # 7, t: 0.17
problem25 = ((3, 3, 1, 4, 2, 4, 4, 1, 2, 4, 3), (2, 2, 2, 2, 4, 4, 1, 3))  # 7, t: 9.74
problem26 = ((1, 3, 3, 2, 1, 2, 2), (1, 3, 2, 4, 2, 3, 4, 2))  # 8, t: 0.46
problem27 = ((1, 2, 1, 2), (1, 2, 4, 1, 2, 2, 4, 1, 3, 2, 1, 2))  # 10, t: 0.01
problem28 = ((2, 2, 3, 2), (3, 1))  # no, t: 0
problem29 = ((4, 2, 2, 3, 3, 2), (1, 3))  # no, t: 0
problem30 = ((2, 2, 3, 3, 2, 4), (2, 2, 3, 2))  # no, t: 0
problem31 = ((4, 2, 2, 3, 3, 2), (1, 3, 4))  # no, t: 0
problem32 = ((4, 2, 2, 3, 3, 1), (1, 1, 2, 3))  # no, t: 0
problem33 = ((1, 2, 2, 1, 1, 3, 3, 1), (4, 2, 3, 4, 4, 2, 3, 1))  # 5


# def main():
program_start = time.time()
problem = [problem1, problem2, problem3, problem4, problem5,
           problem6, problem7, problem8, problem9, problem10,
           problem11, problem12, problem13, problem14, problem15,
           problem16, problem17, problem18, problem19, problem20,
           problem21, problem22, problem23, problem24, problem25,
           problem26, problem27, problem28, problem29, problem30,
           problem31, problem32, problem33]

algorithm = ["astar", "gbfs"]
for i in algorithm:
    for j in problem:
        start_time = time.time()
        solve_problems(j, i)
        end_time = time.time()
        print(f"Time for problem {j} with algo {i}: ", end_time - start_time)
        print("")
program_end = time.time()
print("Time of the problems: ", program_end - program_start)