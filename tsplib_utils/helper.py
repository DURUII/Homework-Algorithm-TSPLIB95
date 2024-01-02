import time


def timeit(func):
    def wrap(*args, **kwargs):
        tic = time.perf_counter()
        result = func(*args, **kwargs)
        toc = time.perf_counter()
        print(f'{func.__name__!r} execution time: {(toc - tic):.4f}s')
        return result

    return wrap
