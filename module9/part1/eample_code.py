def my_area_function(length: int, width: int):
    if type(length) not in (int, float) or type(width) not in (int, float):
        raise TypeError
    if length < 0 or width < 0:
        raise ValueError
    print(length, width, sep='')
    return length * width

def my_func(a, b):
    if a + b > 3:
        raise ValueError