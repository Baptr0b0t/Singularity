import cProfile

def profile_function(func, *args, **kwargs):
    profiler = cProfile.Profile()
    profiler.enable()

    for _ in range(10000):  # Exécute plusieurs fois pour rendre le temps mesurable
        func(*args, **kwargs)

    profiler.disable()
    profiler.print_stats()