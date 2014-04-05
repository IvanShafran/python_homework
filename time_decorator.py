from time import time

def time_decorator(user_function):
    def user_function_with_time(*args):
        start_time = time()
        result = user_function(*args)
        print(str(time() - start_time))
        return result

    return user_function_with_time