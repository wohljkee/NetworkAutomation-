# context

class My_Context:
    def __enter__(self):
        print('enter')
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')
        if isinstance(exc_val, AttributeError):
            print(exc_type, exc_val, exc_tb)
            return True


c = My_Context()
with c as context:
    print('in context')
    # raise AttributeError('We have failed')
    raise ZeroDivisionError('This cannot be solved')