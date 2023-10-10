from abc import abstractmethod, ABCMeta

import rich

from tsplib_instance.base import Instance


class Algorithm(metaclass=ABCMeta):
    def __init__(self, tag='Unspecified') -> None:
        self.tag = tag

    @abstractmethod
    def solve(self, problem, verbose=False):
        pass

    def print_best_solution(self, problem: Instance):
        """Prints the best solution found."""
        rich.print(f"[bold green blink]{self.tag} found a solution with length {problem.best_seen.length}[/]", )
