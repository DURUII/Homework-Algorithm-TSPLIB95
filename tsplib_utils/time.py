import time


def timeit(func):
    def wrap(*args, **kwargs):
        tic = time.perf_counter()
        result = func(*args, **kwargs)
        toc = time.perf_counter()
        with open('log.csv', 'a') as logger:
            tag, benchmark, length, tour = result
            logger.write(
                f'{benchmark},{tag},{length},{toc - tic},\'{tour}\'\n'
            )
        return result

    return wrap
