
import time
from AI_Co2_Calculator_arm import *


def main(file_path='./jtop_usage.csv'):
    start_total_time = time.time()
    try:
        with jtop() as jetson:
            log_usage_stats(jetson, file_path)
    except JtopException as e:
        print(f"An error occurred with jtop: {e}")
    except KeyboardInterrupt:
        print("Closed with CTRL-C")
    except IOError:
        print("I/O error")
    end_total_time = time.time()
    total_duration = end_total_time - start_total_time
    print(f"Total script duration: {total_duration} seconds")
    
if __name__ == "__main__":
    main()

    end_time = int(time.time())
    start_time = end_time - 60

    calculate_energy(start_time, end_time)