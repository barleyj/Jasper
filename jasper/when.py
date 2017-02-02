from functools import wraps


class When(object):

    def __init__(self, function_name):
        self.when_function = getattr(self, function_name)

    def __call__(self, context):
        self.context = context
        self.__save_result(self.when_function)()
        pass

    def __save_result(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.context.result = func(*args, **kwargs)

        return wrapper
