import os
from time import sleep


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def wait_for_file(path, filename, max_tries, time_wait):
    current_tries = 0
    while not os.path.exists(path):
        print(f"{filename} file not found at {path}, trying again in 10 seconds")
        current_tries += 1
        if current_tries == max_tries:
            print(f"Max number of retries done ({max_tries}), finishing program")
            return False
        sleep(time_wait)

    return True
