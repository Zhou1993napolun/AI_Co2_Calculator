from jtop import jtop, JtopException
import csv
import requests
import chardet
import urllib.request
import json
import subprocess
import re
import time
import platform
import pyJoules
from datetime import datetime, timedelta
from pyJoules.energy_meter import measure_energy
import pandas as pd
from jtop import jtop
import difflib

def check_jtop_running():
    try:
        # 尝试调用jtop命令
        result = subprocess.run(['jtop', '-v'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            print("jtop running")
        else:
            print("jtop not running")
    except subprocess.CalledProcessError:
        # 如果命令执行失败，说明jtop没有运行
        print("jtop not running")
    except FileNotFoundError:
        # 如果没有找到jtop命令，可能未安装jtop
        print("jtop not installed")

# 调用函数
check_jtop_running()



def get_system_stats():
    try:
        with jtop() as jetson:  # Ensure jtop is correctly used with a context manager
            if jetson.ok():  # Check if jtop is running and ready
                stats = jetson.stats

                # Extract CPU usage values
                cpu_usages = [stats[f'CPU{i}'] for i in range(1, 9) if f'CPU{i}' in stats]
                average_cpu_usage = sum(cpu_usages) / len(cpu_usages) if cpu_usages else 0
                # Extract RAM usage value
                ram_usage = stats.get('RAM', 0)
                # Extract GPU usage value
                gpu_usage = stats.get('GPU', 0)

                # Get the operating system name and version number
                os_name = platform.system()
                os_version = platform.release()

                # Get the network name of the computer
                node_name = platform.node()

                # Get the computer's processor information
                processor = platform.processor()

                # Get the computer's architecture information
                machine = platform.machine()

                # Get the computer's platform information
                platform_info = platform.platform()

                # Get the complete information of the computer
                system_info = platform.uname()

                # 获取CPU型号
                cpu_model = "Unknown"
                try:
                    cpu_info = subprocess.check_output("lscpu | grep 'Model name'", shell=True)
                    cpu_model = cpu_info.decode().strip().split(":")[1].strip()
                except subprocess.CalledProcessError:
                    print("Could not get CPU model.")

                # 获取GPU信息
                gpu_model = "Unknown"
                try:
                    gpu_info = subprocess.check_output("lspci | grep -i 'pci bridge' | head -n 1", shell=True)
                    gpu_model = gpu_info.decode().strip().split("PCI bridge:")[1].strip()
                except subprocess.CalledProcessError:
                    print("Could not find GPU information.")

                # Print the obtained system information
                print(f"Operating System Name: {os_name}")
                print(f"Operating System Version: {os_version}")
                print(f"Computer Network Name: {node_name}")
                print(f"Processor Information: {processor}")
                print(f"Architecture Information: {machine}")
                print(f"Platform Information: {platform_info}")
                print(f"Complete System Information: {system_info}")
                print(f"CPU Model: {cpu_model}")
                print(f"GPU Model: {gpu_model}")

                # CSV file writing using csv module
                with open('./co2signal_api/training_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Operating System Name', os_name, ''])
                    writer.writerow(['Operating System Version', os_version, ''])
                    writer.writerow(['Computer Network Name', node_name, ''])
                    writer.writerow(['Processor Information', processor, ''])
                    writer.writerow(['Architecture Information', machine, ''])
                    writer.writerow(['Platform Information', platform_info, ''])
                    writer.writerow(['Complete System Information', str(system_info), ''])
                    writer.writerow(['CPU Model', cpu_model, ''])
                    writer.writerow(['GPU Model', gpu_model, ''])

    except JtopException as e:
        print(f"An error occurred with jtop: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Calling the function to display system statistics
get_system_stats()


def log_usage_stats(jetson, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['time', 'CPU_usage', 'GPU_usage', 'RAM_usage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        start_time = time.time()  # 记录循环开始的时间

        while jetson.ok():
            current_time = time.time()
            if current_time - start_time >= 60:  # 确保循环运行时间不超过 60 秒
                print("Time limit reached. Exiting loop.")
                break

            stats = jetson.stats
            cpu_usages = [stats[key] for key in stats.keys() if key.startswith('CPU')]
            average_cpu_usage = sum(cpu_usages) / len(cpu_usages) if cpu_usages else 0

            row = {
                'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                'CPU_usage': average_cpu_usage,
                'GPU_usage': stats.get('GPU', 0),  # 使用get方法并提供默认值0
                'RAM_usage': stats.get('RAM', 0),  # 使用get方法并提供默认值0
            }
            writer.writerow(row)
            print(f"Logged data at {row['time']}")




def fuzzy_search_power(model_type, model_name):
    if model_type == 'cpu':
        file_path = './CPUPowerDict.csv'
    else:
        file_path = './GPUPowerDict.csv'

    print(model_type)
    print(model_name)

    if model_type == 'gpu':
        bracket_content = re.search(r'\[(.*?)\]', model_name)
        if bracket_content:
            model_name = bracket_content.group(1)
            print(f"Extracted model name from brackets: {model_name}")

    matched_powers = []
    max_similarity = 0
    best_match = None

    model_pattern = '.*'.join(map(re.escape, model_name.split()))

    print(f"Regex pattern: Model - {model_pattern}")

    try:
        with open(file_path, newline='', encoding='iso-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            columns = {col.lower(): col for col in reader.fieldnames}
            print(f"CSV columns: {columns}")
            for row in reader:
                if 'manufacturer' in columns and 'name' in columns:
                    full_model_name = f"{row[columns['manufacturer']]} {row[columns['name']]}"
                    print(f"Checking row: {full_model_name}")
                    similarity = difflib.SequenceMatcher(None, model_name, full_model_name).ratio()
                    if similarity > max_similarity:
                        max_similarity = similarity
                        best_match = row['power(W)']
                    print(f"Matched: {full_model_name} -> {row['power(W)']} with similarity {similarity}")
                else:
                    print("Error: 'manufacturer' or 'name' column not found in CSV")
                    return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    if max_similarity < 0.3:
        if model_type == 'cpu':
            matched_power = 15.0
        else:
            matched_power = 30.0
    else:
        try:
            matched_power = float(re.sub(r'[^\d.]', '', best_match))
            print(f"Best matched power: {matched_power} with similarity {max_similarity}")
        except ValueError as e:
            print(f"Error converting matched power to float: {e}")
            return None

    print(f"Returning power: {matched_power}")
    return matched_power


def calculate_energy(start_time, end_time):
    csv_file = './jtop_usage.csv'

    df = pd.read_csv(csv_file, parse_dates=['time'])

    start_time = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    end_time = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')

    filtered_df = df[(df['time'] >= start_time) & (df['time'] <= end_time)]

    cpu_mean = filtered_df['CPU_usage'].mean()
    gpu_mean = filtered_df['GPU_usage'].mean()
    ram_mean = filtered_df['RAM_usage'].mean()

    cpu_info = subprocess.check_output("lscpu | grep 'Model name'", shell=True)
    cpu_model = cpu_info.decode().strip().split(":")[1].strip()
    gpu_info = subprocess.check_output("lspci | grep -i 'pci bridge' | head -n 1", shell=True)
    gpu_model = gpu_info.decode().strip().split("PCI bridge:")[1].strip()

    cpu_power = fuzzy_search_power('cpu', cpu_model)
    gpu_power = fuzzy_search_power('gpu', gpu_model)

    start_time = int(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').timestamp())
    end_time = int(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').timestamp())
    duration = end_time - start_time

    print(cpu_power)
    print(gpu_power)
    print(cpu_mean)
    print(gpu_mean)
    energy = (cpu_power * cpu_mean + gpu_power * gpu_mean) / 100 * (end_time - start_time) / 3600

    print("\n")
    print(f"Estimated power consumption by CPU+GPU：{energy}Wh")
    print(f"After conversion：{energy / 1000} kWh")
    print(f"After conversion：{energy * 3600000} J")
    print(f"duration: {duration} s ")
    print(f"datetime: {datetime.now().strftime('%m/%d/%Y %H:%M')}")
    print(f'Energy Comsumption: {energy / 1000} mJ, CPU_average_usage: {cpu_mean}%, , GPU_average_usage: {gpu_mean}%, RAM_average_usage: {ram_mean}%')

    # Now, let's write this combined data to a CSV file
    with open('./co2signal_api/training_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write headers and CPU usages
        writer.writerow(["Instance", "Resource Type", "Average Usage (%)", ''])
        writer.writerow(["node", "CPU", cpu_mean, ''])
        writer.writerow(["node", "RAM", ram_mean, ''])
        writer.writerow(["node", "GPU", gpu_mean, ''])
        writer.writerow(["Estimated power consumption by CPU+GPU Wh", float(f"{energy:.6f}"), ''])
        writer.writerow(["After conversion kWh", float(f"{energy / 1000:.6f}"), ''])
        writer.writerow(["After conversion J", float(f"{energy * 3600000:.6f}"), ''])
        writer.writerow(["duration", str(duration), ''])
        writer.writerow(["datetime", datetime.now().strftime('%m/%d/%Y %H:%M'), ''])
    return energy


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