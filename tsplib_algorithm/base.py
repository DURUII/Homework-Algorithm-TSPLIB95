from abc import abstractmethod, ABCMeta

import rich


class Algorithm(metaclass=ABCMeta):
    def __init__(self, tag='BaseAlgorithm', verbose=False, **kwargs):
        self.tag = tag
        self.verbose = verbose

    @abstractmethod
    def solve(self, problem):
        if self.verbose:
            rich.print(f"[bold green blink]{self.tag} found a solution with length {problem.best_seen.length}[/]", )
