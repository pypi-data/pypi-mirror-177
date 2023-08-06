import concurrent.futures
from time import perf_counter
def e(func,items,whizz=True):
    t1 = perf_counter()
    if whizz == True:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(func, items)
    elif whizz == 'both':
        return f"{e(func,items,whizz=True)} {e(func,items,whizz=False)}"
    else:
        for item in items:
            func(item)
        t2 = perf_counter()
        return f"\nCompleted in {t2-t1:.3f} seconds without naveeen modv3."
    t2 = perf_counter()
    return f"\nCompleted in {t2-t1:.3f} seconds using naveeen modv3."