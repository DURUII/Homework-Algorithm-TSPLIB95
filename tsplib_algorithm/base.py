from abc import abstractmethod, ABCMeta


class Algorithm(metaclass=ABCMeta):
    def __init__(self, tag='BaseAlgorithm', verbose=False):
        self.tag = tag
        self.verbose = verbose

    @abstractmethod
    def solve(self, problem):
        pass
