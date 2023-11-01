# Homework-Algorithm-TSPLIB95

This project replicates/implements some classic algorithms for solving the traveling salesman problem, including:

- Greedy Nearest Neighbor Algorithm
- Christofides-Serdyukov Algorithm
- Simulated Annealing Algorithm
- Genetic Algorithm

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




