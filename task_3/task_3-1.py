"""
3. Multithreading and Concurrency
- Python script that spawns two threads printing even and odd numbers
"""

import threading
import time


def print_even_numbers():
    for i in range(2, 201, 2):
        print(f"Even: {i}")
        time.sleep(0.5)


def print_odd_numbers():
    for i in range(1, 201, 2):
        print(f"Odd: {i}")
        time.sleep(0.5)


# Example usage
if __name__ == '__main__':
    even_thread = threading.Thread(target=print_even_numbers)
    odd_thread = threading.Thread(target=print_odd_numbers)

    even_thread.start()
    odd_thread.start()

    even_thread.join()
    odd_thread.join()
