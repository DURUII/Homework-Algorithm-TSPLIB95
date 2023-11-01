# Homework-Algorithm-TSPLIB95

This project aims to replicate and implement several classic algorithms for solving the traveling salesman problem,
including:

- Greedy Nearest Neighbor Algorithm
- Christofides-Serdyukov Algorithm
- Simulated Annealing Algorithm
- Genetic Algorithm

I am planning to submit this project as my homework for the "Evolutionary Computation" course at WUST.

## Getting Started

### Prerequisites

    pip install -r requirements.txt

### Running the tests

An example is as follows:

    problem = Problem('berlin52', verbose=True)
    
    solver = SimulatedAnnealing(
        t=1000, eps=1e-14, alpha=0.98, time_out=1,
        early_stop=problem.dimension, verbose=True)
    
    solver.solve(problem)
    print(problem.best_seen.length)

## Informative Material

- [The Traveling Salesman Problem: When Good Enough Beats Perfect](https://youtu.be/GiDsjIBOVoA)
- [MIT Approximation Algorithms: Traveling Salesman Problem](https://youtu.be/zM5MW5NKZJg)
- [PlatEMO: A MATLAB Platform for Evolutionary Multi-Objective Optimization](https://github.com/BIMK/PlatEMO/tree/master/PlatEMO/Algorithms/Single-objective%20optimization)
- [AcWing算法进阶课 - 模拟退火](https://www.acwing.com/activity/content/32/)
- [Tsp问题的启发式方法 - 徐阳](https://gitee.com/mathu-dxy/tsp_heuristic)
