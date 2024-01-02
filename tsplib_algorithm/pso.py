import math
import random
import time

from tsplib_algorithm.base import Algorithm
from tsplib_problem.base import Problem
from tsplib_utils.time import timeit
import numpy as np


class Particle:
    inertia, alpha, beta = 0.4, 0.32, 0.38
    gb_position, gb_fitness = None, math.inf
    problem = None
    promising = False

    def __init__(self, problem: Problem):
        if Particle.problem is None:
            Particle.problem = problem

        self.position = np.random.rand(problem.dimension)
        self.velocity = np.random.rand(problem.dimension)
        self.pb_fitness, self.pb_position = math.inf, self.position

        self.eval()

    def eval(self):
        # derive a feasible discrete solution from the concrete position
        tour = list(np.argsort(self.position) + 1)
        fitness = Particle.problem.calculate_length(tour, leaderboard=True)

        # implicitly update p_best and g_best value
        if fitness < self.pb_fitness:
            self.pb_position = self.position
            self.pb_fitness = fitness

        if fitness < Particle.gb_fitness:
            Particle.gb_position = self.position
            Particle.gb_fitness = fitness
            Particle.promising = True

    def move(self):
        self.position = np.clip(self.position + self.velocity, 0, 1)

        self.velocity = np.clip(
            Particle.inertia * self.velocity + Particle.alpha * random.random() * (
                    self.pb_position - self.position) + Particle.beta * random.random() * (
                    Particle.gb_position - self.position), 0, 0.27)


class ParticleSwarmOpt(Algorithm):
    def __init__(self, tag='ParticleSwarmOpt',
                 size=11200, time_out=180, early_stop=500,
                 verbose=True, boost=False):
        super().__init__(tag, verbose, boost)
        self.size = size
        self.time_out = time_out
        self.early_stop = early_stop

    @timeit
    def solve(self, problem: Problem):
        problem.clear_cache()

        # before it is too late
        tic = time.perf_counter()
        while time.perf_counter() - tic < self.time_out:
            # initialization
            particles = [Particle(problem) for _ in range(self.size)]
            step = 0

            while step <= self.early_stop:
                Particle.promising = False
                step += 1

                # evaluation, update p_best and g_best
                if step % 3 == 0:
                    for p in particles:
                        p.eval()

                # update position and renew velocity
                for p in particles:
                    p.move()

                if Particle.promising:
                    step = 0
                print(step)

            print('restart')

        # logger
        return self.tag, problem.benchmark, problem.best_seen.length, problem.best_seen.tour
