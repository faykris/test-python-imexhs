"""
3. Multithreading and Concurrency
- Python program that receives a folder path and a JSON filename, and reads it
"""

import json
import os
import threading
import logging
from queue import Queue

# Configure logging to a file with thread safety
logging.basicConfig(filename='shared_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log_lock = threading.Lock()

def process_element(element_id, element_data):
    try:
        data_lines = element_data['data']
        all_numbers = []

        # Convert strings of numbers into a flat list of integers
        for line in data_lines:
            all_numbers.extend(map(int, line.split()))

        max_value = max(all_numbers)
        normalized_data = [x / max_value for x in all_numbers]

        avg_before = sum(all_numbers) / len(all_numbers)
        avg_after = sum(normalized_data) / len(normalized_data)
        size_of_data = len(all_numbers)

        # Logging the data
        with log_lock:
            logging.info(f"Element ID: {element_id}, Average Before: {avg_before:.2f}, Average After: {avg_after:.2f}, Size: {size_of_data}")

        # Print the data
        print(f"Element ID: {element_id}")
        print(f"Average Before: {avg_before:.2f}, Average After: {avg_after:.2f}, Size: {size_of_data}")

    except Exception as e:
        with log_lock:
            logging.error(f"Error processing element ID '{element_id}': {e}")

def worker_thread(queue):
    while True:
        element_id, element_data = queue.get()
        if element_id is None:
            break
        process_element(element_id, element_data)
        queue.task_done()

def process_json_file(folder_path, json_filename):
    try:
        json_filepath = os.path.join(folder_path, json_filename)
        with open(json_filepath, 'r') as file:
            json_data = json.load(file)

        queue = Queue()
        threads = []

        # Create 4 worker threads
        for _ in range(4):
            thread = threading.Thread(target=worker_thread, args=(queue,))
            thread.start()
            threads.append(thread)

        # Queue the elements to be processed
        for element_id, element_data in json_data.items():
            queue.put((element_id, element_data))

        # Block until all tasks are done
        queue.join()

        # Stop workers
        for _ in range(4):
            queue.put((None, None))

        for thread in threads:
            thread.join()

    except Exception as e:
        logging.error(f"Error processing JSON file '{json_filename}': {e}")


# Example usage
if __name__ == '__main__':
    print("---- File sample-03-00-json.json ----")
    process_json_file('/Users/cristianpinzon/Downloads/prueba_python', 'sample-03-00-json.json')
    print("---- File sample-03-01-json.json ----")
    process_json_file('/Users/cristianpinzon/Downloads/prueba_python', 'sample-03-01-json.json')
