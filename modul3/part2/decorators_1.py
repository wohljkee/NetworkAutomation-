# decorator
import functools


# def decorator(func1):
#     def wrapper(*args, **kwargs):
#         print("enter decorator")
#         first, *rest = args
#         first += 1
#         args = first, *rest
#         if first < 10:
#             result = func1(*args, **kwargs)
#         else:
#             return None
#         print("exit decorator")
#         if '5' in result:
#             return 'no alarm for 5 am'
#         return result
#     return wrapper
#
# @decorator
# def alarm(time):
#     print(f"alarm set for {time}")
#     return f'next alarm in {time + 1}'
#
# # alarm = decorator(alarm)
#
# print(alarm(3))

# #Example:
# def decorator(func1):
#     @functools.wraps(func1)
#     def wrapper(*args, **kwargs):
#         return func1(*args, **kwargs)
#     return wrapper



def decorator(func1):
    @functools.wraps(func1)
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        return func1(*args, **kwargs)

    wrapper.counter = 0
    return wrapper

@decorator
def test():
    print('testing')


test()
print('Function name: ', test.__name__)
test()
test()
test()
print(test.counter)



