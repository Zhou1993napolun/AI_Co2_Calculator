# README



### **Introduction**

* **What is Powertest for ?**

  We need to detect the utilization rate of CPU, GPU and RAM, and then calculate the energy consumption of the device according to the relevant formula, which can be used for the detection of the model. However, because different tools detect different information, such as Prometheus can read the CPU and RAM information, but not directly read the GPU. 

* **What is Prometheus**

  [Prometheus](https://prometheus.io/) is an open-source monitoring and alerting toolkit that focuses on reliability and scalability. Originally built by SoundCloud in 2012, Prometheus has since become a project under the Cloud Native Computing Foundation (CNCF). Key features include:

  - Multi-dimensional Data Model: Uses key-value pairs for data representation, enabling flexible and accurate querying.
  - PromQL: A powerful query language that allows users to aggregate and select time series data in real time.
  - Distributed and Decentralized: Each instance operates independently, but can also be part of a larger setup.
  - Pull-based Model: Scrapes metrics from instrumented jobs, either directly or via an intermediary push gateway.

### **Environment Setup**

* **Install Prometheus**

  ``` sh
  wget https://github.com/prometheus/prometheus/releases/download/v<VERSION>/promethe
   us-<VERSION>.linux-amd64.tar.gz
  ```

  After the download is complete, use the command to extract the file: ``tar xvzf prometheus-*.tar.gz``

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
        - targets: ['localhost:9090']
  
    - job_name: 'node'
      static_configs:
        - targets: ['192.168.23.6:9100']
  
    - job_name: 'nvidia_gpu_exporter'
      static_configs:
        - targets: ['192.168.23.6:9835']
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

* Place the above three extracted files into the `power_test_v1.0` folder.
* Copy all the files in the ``power_test_v1.0`` folder into the folder of your target program

### **Running the Program**

* **Start Nvidia GPU Exporter, Node Exporter, and Prometheus**

  Enter the root directory of  your target program

  ```sh
  chmod +x start_services.sh
  ./start_services.sh
  # If you see the message "All services started in the background." after running, it means the services started successfully.
  ```

  If the script cannot be executed, you can manually start Nvidia GPU Exporter, Node Exporter, and Prometheus by navigating to the corresponding directories and using the ``nohup`` command:

  ```sh
  # Start Prometheus
  nohup ./prometheus --config.file=prometheus.yml > prometheus.log 2>&1 &
  
  # Start GPU exporter
  nohup ./nvidia_gpu_exporter > nvidia_gpu_exporter.log 2>&1 &
  
  # Start Node exporter
  nohup ./node_exporter > node_exporter.log 2>&1 &
  ```

* **Modify the main code of the power_test target program**

  ```python
  from powertest import *
  import time
  ...
  
  if __name__ == "__main__":
      start = time.time() # # Record the start time of the program
      # your code 
      end = time.time()   # Record the end time of the program
      test_mesure(start,end) 
      
  ```

* **Start the Target Program**

  ```sh
  python3 name_of_your_code.py
  ```

  Then, you can find the .csv file recording various information in the root directory of your target program

### Example

To help you better understand how it works, we provide an example using ``powertest.py``

```python
import time
from powertest import *

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

