from abc import abstractmethod, ABCMeta

import rich


class Algorithm(metaclass=ABCMeta):
    def __init__(self, tag='BaseAlgorithm', verbose=False):
        self.tag = tag
        self.verbose = verbose

    def log(self, problem):
        rich.print(f"[bold green blink]{self.tag} found a solution with length {problem.best_seen.length}[/]", )

    @abstractmethod
    def solve(self, problem):
        pass
