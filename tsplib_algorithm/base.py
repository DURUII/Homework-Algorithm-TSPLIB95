from abc import abstractmethod, ABCMeta


class Algorithm(metaclass=ABCMeta):
    def __init__(self, tag, verbose, boost):
        self.tag = tag
        self.verbose = verbose
        self.boost = boost

    @abstractmethod
    def solve(self, problem):
        pass
