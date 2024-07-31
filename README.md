# README

### **Introduction**
  
  In the current global context, where environmental protection is becoming increasingly critical, we present AI_Co2_Calculator—an innovative tool designed to measure the carbon emissions generated during deep learning training processes. Monitoring and reducing carbon emissions has become a shared responsibility for individuals and organizations alike, and AI_Co2_Calculator aims to facilitate this effort.
  AI_Co2_Calculator offers a user-friendly interface that enables users to swiftly and efficiently start monitoring their carbon footprint. The tool provides intuitive and clear data visualizations, which facilitate a comprehensive understanding of carbon emissions. Its robust compatibility allows it to automatically detect the majority of CPU and GPU models available on the market, ensuring wide applicability and convenience.
  One of the key features of AI_Co2_Calculator is its ability to accurately calculate carbon emissions based on the varying carbon intensity of electricity in different countries. This precision is crucial for users aiming to optimize the energy efficiency of their deep learning training processes. By considering the specific carbon intensity of the user's location, AI_Co2_Calculator delivers tailored and precise emission calculations.
  As the world increasingly emphasizes the importance of sustainability, tools like AI_Co2_Calculator play a vital role in advancing environmental responsibility within the tech industry. By helping users optimize their energy use and reduce their carbon footprint, AI_Co2_Calculator contributes to the broader goal of building a greener and more sustainable future. Embracing AI_Co2_Calculator means taking a proactive step towards environmental stewardship, aligning technological advancements with the imperative of reducing carbon emissions for the benefit of our planet.


**AI_Co2_Calculator Overview ?**

  AI_Co2_Calculator is designed to detect the utilization rates of CPU, GPU, and RAM, and then calculate the energy consumption of the device based on relevant formulas. This functionality is essential for accurately assessing the energy usage and carbon emissions of deep learning models. Different tools are required to detect different information.
  
  On x86 systems, we use Prometheus to read CPU and RAM utilization, and NVIDIA exporter and Node exporter to monitor GPU usage. 
  For ARM systems, we leverage built-in Linux tools like jtop to monitor CPU, GPU, and RAM utilization.
  
  This comprehensive data collection allows users to obtain an integrated view of the utilization of all major hardware components. By combining these metrics, AI_Co2_Calculator provides a holistic view of energy consumption, helping users to optimize their models and reduce their environmental impact.


###**How to Use AI_Co2_Calculator on Different Systems**

###**Global architecture diagram**

![PIC](https://github.com/user-attachments/assets/671d4335-581b-4094-b263-2c7252a83917)


**To effectively use AI_Co2_Calculator on x86 systems**

AI_Co2_Calculator is an innovative tool designed to monitor and calculate carbon emissions during deep learning training processes. Here's a detailed guide on how to effectively use AI_Co2_Calculator on x86 systems, including the necessary tools and configuration steps.

**Tool Overview**

[Prometheus](https://prometheus.io/) is an open-source monitoring and alerting toolkit that focuses on reliability and scalability. Originally built by SoundCloud in 2012, Prometheus has since become a project under the Cloud Native Computing Foundation (CNCF). Key features include:

  - Multi-dimensional Data Model: Uses key-value pairs for data representation, enabling flexible and accurate querying.
  - PromQL: A powerful query language that allows users to aggregate and select time series data in real time.
  - Distributed and Decentralized: Each instance operates independently, but can also be part of a larger setup.
  - Pull-based Model: Scrapes metrics from instrumented jobs, either directly or via an intermediary push gateway.


[NVIDIA DCGM](https://developer.nvidia.com/dcgm)(nvidia_gpu_exporter, Node Exporter)

NVIDIA Data Center GPU Manager (DCGM) is a suite of tools for managing and monitoring NVIDIA datacenter GPUs in cluster environments. It includes active health monitoring, comprehensive diagnostics, system alerts and governance policies including power and clock management. It can be used standalone by infrastructure teams and easily integrates into cluster management tools, resource scheduling and monitoring products from NVIDIA partners.



### **Environment Setup for X86**

* **Install Prometheus**

  ``` sh
  wget wget https://github.com/prometheus/prometheus/releases/download/v2.53.1/prometheus-2.53.1.linux-amd64.tar.gz
  ```

  After the download is complete, use the command to extract the file: ``tar -xvf prometheus-2.53.1.linux-amd64.tar.gz``

* **Configuring Prometheus**

  To configure Prometheus, you need to edit the `prometheus.yml` file. This file is used by Prometheus to determine what to scrape and how to handle alerts.

  Below is an example configuration for `prometheus.yml`. Make sure to adjust the settings according to your specific requirements:

  ```yaml
  # Global configuration
  global:
    scrape_interval: 15s  # Set the scrape interval to every 15 seconds. Default is 1 minute.
    evaluation_interval: 15s  # Evaluate rules every 15 seconds. Default is 1 minute.
    # scrape_timeout is set to the global default of 10s.
  
  # Alertmanager configuration
  alerting:
    alertmanagers:
      - static_configs:
          - targets:
              - alertmanager:9093
  
  # Load rules once and periodically evaluate them based on the global 'evaluation_interval'.
  # rule_files:
  #  - "first_rules.yml"
  #  - "second_rules.yml"
  
  # Scrape configurations
  scrape_configs:
    - job_name: 'prometheus'
      # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
      static_configs:
        - targets: ['your_ip:9090']
  
    - job_name: 'node'
      static_configs:
        - targets: ['your_ip:9100']
  
    - job_name: 'nvidia_gpu_exporter'
      static_configs:
        - targets: ['your_ip:9835']
  ```

  Make sure to replace the placeholder IP addresses and ports with the actual values used in your environment.

  To apply the configuration, save your changes and restart the Prometheus server.

* **Install Nvidia GPU Exporter**

  ```sh
   wget nvidia_gpu_exporter_1.1.0_linux_64.tar  
  ```

  (If this method is not feasible, you can directly use the installation package provided in the "source" folder)

  After the download is complete, use the command to extract the file: ``tar -xvf nvidia_gpu_exporter_1.1.0_linux_64.tar.gz``
  

* **Install Node Exporter**

  ``` sh
  wget node_exporter_1.5.0.linux_amd64.tar
  ```

  (If this method is not feasible, you can directly use the installation package provided in the "source" folder)

  After the download is complete, use the command to extract the file: ``tar -xvf node_exporter_1.5.0.linux_amd64.tar.gz``

  By default, the nvidia_node_exporter and node_exporter should work out of the box for most setups. However, if there are any specific configurations or flags you'd like to set, refer to the official documentation.

  Place the above three extracted files into the `AI_Co2_Calculator` folder.
  Copy all the files in the ``AI_Co2_Calculator`` folder into the folder of your target program


* **Install AI carbon footprint tools Python server start process**
```
#Install Python 3.8 or Higher

#Install FastAPI and Unicorn

python -m pip install fastapi 
python -m pip install unicorn

#Start the Service
Open the command line terminal and navigate to the directory containing your main.py file. Start the service with the following command:
python -m uvicorn main:app --reload
```


* **Install ResponseAIProject** 

```
First, make sure you have install the JDK8 above, and the nodejs (version above 18), npm(version above 8) command in your machine.

1  go to responseAIProject-/serve-end/, and start the jar with: nohup  java -jar responseAIWeb-0.0.1-SNAPSHOT.jar >log.out &
2  Go to the responseAIProject-\responseAIWeb, exec the commands:
  1)  npm i serve -g
  2)  npm i
  3)  run command "npm run build"
     
 Afetr success build, there is "build" folder under responseAIWeb, go into "build" folder,
  5) nohup serve -s  -l 3033 & (Remember, this command must be you are in "build" folder)
  6) Then, access the page on any machine  , https://IP:3033
```


### **Running the Program for x86**

**Start Nvidia GPU Exporter, Node Exporter, Prometheus, AI carbon footprint tools Python server, responseAIProject**

  Enter the root directory of  your target program

  ```sh
  chmod +x start_services.sh
  ./start_services.sh
  # If you see the message "All services started in the background." after running, it means the services started successfully.
  ```

 If the script cannot be executed, you can manually start Nvidia GPU Exporter, Node Exporter, Prometheus, AI carbon footprint tools Python server, and responseAIProject by navigating to the corresponding directories and using the nohup command by following these steps:

  ```sh
  # Start Prometheus
  nohup ./prometheus --config.file=prometheus.yml > prometheus.log 2>&1 &
  
  # Start GPU exporter
  nohup ./nvidia_gpu_exporter > nvidia_gpu_exporter.log 2>&1 &
  
  # Start Node exporter
  nohup ./node_exporter > node_exporter.log 2>&1 &

  # Start AI carbon footprint tools Python server
  Open the command line terminal and navigate to the directory containing your main.py file.
  Start the service with the following command: python -m uvicorn main:app --reload

  # Start responseAIProject
  nohup serve -s  -l 3033 & (Remember, this command must be you are in "build" folder)
  ```
  
**Modify the main code of the power_test target program**

  ```python
  from AI_Co2_Calculator import *
  import time
  ...
  
  if __name__ == "__main__":
      start = time.time() # # Record the start time of the program
      # your code 
      end = time.time()   # Record the end time of the program
      test_mesure(start,end) 
      
  ```

**Start the Target Program**

  ```sh
  python3 name_of_your_code.py
  ```

  Then, you can find the .csv file recording various information in the root directory of your target program

### Example for x86

To help you better understand how it works, we provide an example using ``powertest.py``

```python
import time
from AI_Co2_Calculator import *

def main():
    print("Program Start...")
    time.sleep(50)    
    print("The delay ends and the program continues...")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    
    test_mesure(start,end)
```

**To effectively use AI_Co2_Calculator on ARM systems**

AI_Co2_Calculator is an innovative tool designed to monitor and calculate carbon emissions during deep learning training processes. Here's a detailed guide on how to effectively use AI_Co2_Calculator on ARM systems, including the necessary tools and configuration steps.


**Tool Overview**


Jtop : jtop is a monitoring tool specifically designed for NVIDIA Jetson platforms. It provides a real-time view of system metrics such as CPU, GPU, RAM, and thermal information. This tool is particularly useful for developers and engineers working with AI and deep learning applications on Jetson devices, allowing them to monitor resource utilization and system performance effectively.

Key Features:
  -Real-time monitoring: Provides up-to-date information on CPU, GPU, memory, and thermal status.
  -User-friendly interface: Displays data in a clear and organized manner.
  -Optimized for Jetson platforms: Tailored specifically for NVIDIA Jetson devices.


### **Environment Setup for ARM**
* **Install Jtop**
```
#Update package lists and install Python 3 and pip
sudo apt update
sudo apt install python3 python3-pip

#Install jetson-stats:
sudo -H pip3 install jetson-stats

#Run jtop:
sudo jtop
```

* **Install AI carbon footprint tools Python server start process**
```
#Install Python 3.8 or Higher

#Install FastAPI and Unicorn

python -m pip install fastapi 
python -m pip install unicorn

#Start the Service
Open the command line terminal and navigate to the directory containing your main.py file. Start the service with the following command:
python -m uvicorn main:app --reload
```


* **Install ResponseAIProject** 

```
First, make sure you have install the JDK8 above, and the nodejs (version above 18), npm(version above 8) command in your machine.

1  go to responseAIProject-/serve-end/, and start the jar with: nohup  java -jar responseAIWeb-0.0.1-SNAPSHOT.jar >log.out &
2  Go to the responseAIProject-\responseAIWeb, exec the commands:
  1)  npm i serve -g
  2)  npm i
  3)  run command "npm run build"
     
 Afetr success build, there is "build" folder under responseAIWeb, go into "build" folder,
  5) nohup serve -s  -l 3033 & (Remember, this command must be you are in "build" folder)
  6) Then, access the page on any machine  , https://IP:3033
```


### **Running the Program for ARM**
* **Start Jtop, AI carbon footprint tools Python server, responseAIProject**
```
#Check if jtop is Already Installed:
jtop --version

#Start AI carbon footprint tools Python server
Open the command line terminal and navigate to the directory containing your main.py file.
Start the service with the following command: python -m uvicorn main:app --reload

#Start responseAIProject
nohup serve -s  -l 3033 & (Remember, this command must be you are in "build" folder)
```

* **Start the Target Program**

  ```sh
  python3 name_of_your_code.py
  ```
  Then, you can find the .csv file recording various information in the root directory of your target program

### Example for ARM 

To help you better understand how it works, we provide an example using ``AI_Co2_Calculator_arm.py``

```python

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
```

### Conclusion
AI_Co2_Calculator is a powerful tool designed to monitor and reduce carbon emissions during deep learning training. By providing precise calculations based on local carbon intensity, it helps optimize energy use. The tool seamlessly integrates data from various hardware components using Prometheus and NVIDIA exporter on x86 systems and jtop on ARM systems. This comprehensive monitoring aids in reducing the environmental impact of deep learning models. Embracing AI_Co2_Calculator is a proactive step towards sustainability, aligning technological advancements with the need to reduce carbon emissions and build a greener future.

