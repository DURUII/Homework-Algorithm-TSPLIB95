from tsplib_algorithm.wl import WangLeiAlgorithm
from tsplib_instance.base import Instance


instance = Instance(benchmark='a280', verbose=True)
solver = WangLeiAlgorithm()
solver.solve(instance, verbose=True, early_stop=instance.dimension, patience=5000)
    

