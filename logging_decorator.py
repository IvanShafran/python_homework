import logging

def loggining_decorator(filename):
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        filename=filename)

    def decorator(user_function):
        def user_function_with_log(*args, **kwargs):
            logging.debug(str(user_function.__qualname__) + " Starting")
            return user_function(*args, **kwargs)

        return user_function_with_log

    return decorator