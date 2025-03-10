# Exceptions
import time

a = 10
if a == 0:
    var1 = 0

try:
    # var1 + 3
    # 1/0
    print('Hello Python')
    raise AttributeError('This will fail')

# except Exception:
#     print('We are going to solve all problems')
# except:
#     print('We are going to solve all problems')
except AttributeError as e:
    print(e, 'with AttributeError')
    time.sleep(5)
except (ZeroDivisionError, AssertionError):
    print('We cannot devide by zero')
except NameError:
    print('we have no var3 variable')
except:
    print('We are going to solve all problems')
else:
    print('Success')

print('done')