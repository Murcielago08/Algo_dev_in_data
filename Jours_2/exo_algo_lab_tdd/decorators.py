import time
import functools

def retry(max_attempts=3, exceptions=(Exception,), delay=0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    if delay:
                        time.sleep(delay)
        return wrapper
    return decorator
