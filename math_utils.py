def clamp(val, a, b):
    if a > val:
        return a
    if b < val:
        return b
    return val


def clamp01(val):
    return clamp(val, 0, 1)


# map value from interval before_int to interval after_int
def map_val_to_int(value, before_int, after_int):
    return (value - before_int[0]) / before_int[1] * after_int[1] + after_int[0]


# map value from interval before_int to interval after_int, and clamp resulting value to the after_int
def map_n_clamp_val_to_int(value, before_int, after_int):
    return clamp(map_val_to_int(value, before_int, after_int), after_int[0], after_int[1])