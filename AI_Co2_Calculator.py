import requests
import urllib.request
import json
import subprocess
import re
import time
import logging
import platform
import csv
from datetime import datetime, timedelta
import difflib
import pandas as pd



prometheus_server_address = 'http://localhost:9090'

# 配置日志
logging.basicConfig(level=logging.INFO)
logging.info("This is an info level log")

def getTargetsStatus(address):
    print("\n\n")
    url = address + '/api/v1/targets'
    response = requests.request('GET', url)
    if response.status_code == 200:
        targets = response.json()['data']['activeTargets']
        print('-----------------------Targets Details-------------------------')
        print('--------------------------------------------------------------')
        aliveNum, totalNum = 0, 0
        downList = []
        for target in targets:
            totalNum += 1
            if target['health'] == 'up':
                aliveNum += 1
            else:
                downList.append(target['labels']['instance'])
        print('-----------------------TargetsStatus--------------------------')
        print(str(aliveNum) + ' in ' + str(totalNum) + ' Targets are alive !!!')
        print('--------------------------------------------------------------')
        for down in downList:
            print('\033[31m\033[1m' + down + '\033[0m' + ' down !!!')
        print('-----------------------TargetsStatus--------------------------')
    else:
        print('\033[31m\033[1m' + 'Get targets status failed!' + '\033[0m')
    print()


def get_system_info():
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

    # Execute command to obtain CPU information
    cpu_info = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | head -n 1", shell=True)
    cpu_model = cpu_info.decode().split(":")[1].strip()

    # Execute command to obtain GPU information
    gpu_info = subprocess.check_output("lspci | grep 'VGA compatible controller'", shell=True)
    gpu_model = re.search(r'\[(.*?)\]', gpu_info.decode()).group(1).strip()  # 提取方括号中的内容


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

# Call function to get system information and write to CSV
get_system_info()



def queryUsage(address, expr, start_time, end_time):
    url = address + '/api/v1/query?query=' + expr
    params = {
        'query': expr,
        'start': start_time,
        'end': end_time,
        'step': '1m'  # The time interval can be adjusted as needed
    }
    try:
        # return json.loads(requests.get(url=url).content.decode('utf8', 'ignore'))
        response = requests.get(url=url, params=params)
        data = json.loads(response.content.decode('utf8', 'ignore'))
        return data
    except Exception as e:
        print(e)
        return {}


def query_CPU_Average_Usage(address, start_time, end_time):
    query_expression = '100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode="idle"}}[{}s]))) * 100'.format(
        end_time - start_time)

    result = queryUsage(prometheus_server_address, query_expression, start_time, end_time)
    # process result
    if result:
        cpu_usages = []
        for result_data in result['data']['result']:
            metric = result_data['metric']
            values = result_data['value']
            instance = metric['instance']
            average_usage = float(values[1])
            cpu_usages.append((instance, average_usage))

        print("search result：")
        for instance, usage in cpu_usages:
            print(f"Instance: {instance}, CPU_Average_Usage: {usage}%")

    else:
        print("The query fails or returns an empty dictionary")
    print()


def query_RAM_Average_Usage(address, start_time, end_time):
    query_expression = '(avg by (instance) (irate(node_memory_MemAvailable_bytes[{}s]))) / (avg by (instance) (node_memory_MemTotal_bytes)) * 100'.format(
        end_time - start_time)
    result = queryUsage(prometheus_server_address, query_expression, start_time, end_time)
    # process result
    if result:
        cpu_usages = []
        for result_data in result['data']['result']:
            metric = result_data['metric']
            values = result_data['value']
            instance = metric['instance']
            # print(result_data.keys())
            average_usage = float(values[1])
            cpu_usages.append((instance, average_usage))
        # print(result)
        print("search result：")
        for instance, usage in cpu_usages:
            print(f"Instance: {instance}, RAM_Average_Usage: {usage}%")
    else:
        print("The query fails or returns an empty dictionary")
    print()


def query_GPU_Average_Usage(address, start_time, end_time):
    # query_expression = 'avg_over_time(nvidia_gpu_utilization{{job="nvidia_gpu_exporter"}}[{}s])'.format(end_time - start_time)
    query_expression = 'avg_over_time(nvidia_smi_utilization_gpu_ratio{{job="nvidia_gpu_exporter"}}[{}s])'.format(
        end_time - start_time)
    result = queryUsage(prometheus_server_address, query_expression, start_time, end_time)
    # 处理结果
    if result:
        cpu_usages = []
        for result_data in result['data']['result']:
            metric = result_data['metric']
            values = result_data['value']
            instance = metric['instance']
            # print(result_data.keys())
            average_usage = float(values[1])
            cpu_usages.append((instance, average_usage))
        # print(result)
        print("search result：")
        for instance, usage in cpu_usages:
            print(f"Instance: {instance}, CPU_Average_Usage: {usage}%")
    else:
        print("The query fails or returns an empty dictionary")
    print()


def fuzzy_search_power(model_type, model_name):
    if model_type == 'cpu':
        file_path = './CPUPowerDict.csv'
    else:
        file_path = './GPUPowerDict.csv'

    print(model_type)
    print(model_name)

    # If GPU, extract the name inside the brackets
    if model_type == 'gpu':
        bracket_content = re.search(r'\[(.*?)\]', model_name)
        if bracket_content:
            model_name = bracket_content.group(1)
            print(f"Extracted model name from brackets: {model_name}")

    matched_powers = []
    max_similarity = 0
    best_match = None

    # Create a pattern for model name
    model_pattern = '.*'.join(map(re.escape, model_name.split()))

    print(f"Regex pattern: Model - {model_pattern}")

    try:
        with open(file_path, newline='', encoding='iso-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            # Normalize column names to lowercase
            columns = {col.lower(): col for col in reader.fieldnames}
            print(f"CSV columns: {columns}")  # 调试：打印所有列名
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
            matched_power = 120
        else:
            matched_power = 250
    else:
        try:
            print(f"Raw best match power: {best_match}")  # 调试：打印原始的匹配功率值
            # Remove non-digit characters before converting to float
            matched_power = float(re.sub(r'[^\d.]', '', best_match))
            print(f"Best matched power: {matched_power} with similarity {max_similarity}")
        except ValueError as e:
            print(f"Error converting matched power to float: {e}")
            return None

    print(f"Returning power: {matched_power}")
    return matched_power

# 示例测试
print(fuzzy_search_power('cpu', 'Intel E5-2678 v3'))
print(fuzzy_search_power('gpu', 'NVIDIA Corporation GP102 [GeForce GTX 1080 Ti]'))

def query_total_energy(prometheus_server_address, start_time, end_time):

    query_expression1 = '100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode="idle"}}[{}s]))) * 100'.format(
        end_time - start_time)
    result1 = queryUsage(prometheus_server_address, query_expression1, start_time, end_time)

    query_expression2 = '(avg by (instance) (irate(node_memory_MemAvailable_bytes[{}s]))) / (avg by (instance) (node_memory_MemTotal_bytes)) * 100'.format(
        end_time - start_time)
    result2 = queryUsage(prometheus_server_address, query_expression2, start_time, end_time)

    query_expression3 = 'avg_over_time(nvidia_smi_utilization_gpu_ratio{{job="nvidia_gpu_exporter"}}[{}s])'.format(
        end_time - start_time)
    result3 = queryUsage(prometheus_server_address, query_expression3, start_time, end_time)

    cpu_usages = []
    if result1 and 'data' in result1 and 'result' in result1['data']:
        for result_data1 in result1['data']['result']:
            metric1 = result_data1['metric']
            values1 = result_data1['value']
            instance1 = metric1['instance']
            average_usage1 = float(values1[1])
            cpu_usages.append((instance1, average_usage1))

        if cpu_usages:
            usage_cpu = sum(usage for _, usage in cpu_usages) / len(cpu_usages)
            print("Average CPU Usage: {:.2f}%".format(usage_cpu))
        else:
            print("No CPU usage data available.")
            usage_cpu = 0  # Ensure that no division by zero happens

        ram_usages = []
        for result_data2 in result2['data']['result']:
            metric2 = result_data2['metric']
            values2 = result_data2['value']
            instance2 = metric2['instance']
            # print(result_data.keys())
            average_usage2 = float(values2[1])
            ram_usages.append((instance2, average_usage2))
        # print(result)
        print("Query Result：")
        usage_ram = 0
        i = 0
        for instance, usage in ram_usages:
            print(f"Instance: {instance}, Average RAM Usage: {usage}%")
            usage_ram += usage
            i += 1
        usage_ram /= i

        gpu_usages = []
        for result_data3 in result3['data']['result']:
            metric3 = result_data3['metric']
            values3 = result_data3['value']
            instance3 = metric3['instance']
            # print(result_data.keys())
            average_usage3 = float(values3[1])
            gpu_usages.append((instance3, average_usage3))
        # print(result)
        print("Query Result：")
        usage_gpu = 0
        for instance, usage in gpu_usages:
            print(f"Instance: {instance}, Average GPU Usage: {usage * 100}%")
            usage_gpu += usage * 100

        cpu_info = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | head -n 1", shell=True)
        cpu_model = cpu_info.decode().strip().split(":")[1].strip()
        gpu_info = subprocess.check_output("lspci | grep 'VGA compatible controller'", shell=True)
        gpu_model = gpu_info.decode().strip().split(":")[2].strip()

        cpu_power = fuzzy_search_power('cpu', cpu_model)
        gpu_power = fuzzy_search_power('gpu', gpu_model)

        print('cpu_power',cpu_power)
        print('gpu_power',gpu_power)
        print('usage_cpu',usage_cpu)
        print('usage_gpu',usage_gpu)


        print("\n")
        ans = (cpu_power * usage_cpu + gpu_power * usage_gpu) / 100 * (end_time - start_time) / 3600
        print(f"Estimated power consumption by CPU+GPU：{ans}Wh")
        print(f"After conversion：{ans /1000} kWh")
        print(f"After conversion：{ans * 3600000} J")
        duration = end_time - start_time
        print(f"duration: {duration} s ")
        print(f"datetime: {datetime.now().strftime('%m/%d/%Y %H:%M')}")
        print("\n\n")
    else:
        print("The query failed or an empty dictionary was returned.")

        # Now, let's write this combined data to a CSV file
    with open('./co2signal_api/training_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Instance", "Resource Type", "Average Usage (%)", ''])
        for instance, usage in cpu_usages:
            writer.writerow(["node", "CPU", usage, ''])

        for instance, usage in ram_usages:
            writer.writerow(["node", "RAM", usage, ''])

        if gpu_usages:
            instance, usage = gpu_usages[0]
            writer.writerow(["gpu", "GPU", usage * 100, ''])

        writer.writerow(["Estimated power consumption by CPU+GPU Wh", float(f"{ans:.6f}"), ''])
        writer.writerow(["After conversion kWh", float(f"{ans / 1000:.6f}"), ''])
        writer.writerow(["After conversion J", float(f"{ans * 3600000:.6f}"), ''])
        writer.writerow(["duration", str(duration), ''])  
        writer.writerow(["datetime", datetime.now().strftime('%m/%d/%Y %H:%M'), ''])



def test_mesure(start, end):
    get_system_info()

    dur = end - start
    dur = int(dur)
    print(dur)
    prometheus_server_address = 'http://localhost:9090'

    getTargetsStatus(prometheus_server_address)

    end_time = int(time.time())
    start_time = end_time - dur

    query_total_energy(prometheus_server_address, start_time, end_time)
