# README


### **Introduction**

In the current global context, where environmental protection is becoming increasingly critical, we present AI_Co2_Calculator—an innovative tool designed to measure the carbon emissions generated during deep learning training processes. Monitoring and reducing carbon emissions has become a shared responsibility for individuals and organizations alike, and AI_Co2_Calculator aims to facilitate this effort.
AI_Co2_Calculator offers a user-friendly interface that enables users to swiftly and efficiently start monitoring their carbon footprint. The tool provides intuitive and clear data visualizations, which facilitate a comprehensive understanding of carbon emissions. Its robust compatibility allows it to automatically detect the majority of CPU and GPU models available on the market, ensuring wide applicability and convenience.
One of the key features of AI_Co2_Calculator is its ability to accurately calculate carbon emissions based on the varying carbon intensity of electricity in different countries. This precision is crucial for users aiming to optimize the energy efficiency of their deep learning training processes. By considering the specific carbon intensity of the user's location, AI_Co2_Calculator delivers tailored and precise emission calculations.
As the world increasingly emphasizes the importance of sustainability, tools like AI_Co2_Calculator play a vital role in advancing environmental responsibility within the tech industry. By helping users optimize their energy use and reduce their carbon footprint, AI_Co2_Calculator contributes to the broader goal of building a greener and more sustainable future. Embracing AI_Co2_Calculator means taking a proactive step towards environmental stewardship, aligning technological advancements with the imperative of reducing carbon emissions for the benefit of our planet.



* **What is Powertest for ?**

AI_Co2_Calculator is designed to detect the utilization rates of CPU, GPU, and RAM, and then calculate the energy consumption of the device based on relevant formulas. This functionality is essential for accurately assessing the energy usage and carbon emissions of deep learning models. Different tools are required to detect different information—while Prometheus can read CPU and RAM utilization, it cannot directly read GPU utilization.
To bridge this gap, AI_Co2_Calculator integrates specialized GPU monitoring tools such as NVIDIA exporter and Node exporter. This allows users to obtain comprehensive utilization data across all major hardware components. By combining these metrics, AI_Co2_Calculator can provide a holistic view of energy consumption, helping users to optimize their models and reduce their environmental impact.


* **What is Prometheus**

  [Prometheus](https://prometheus.io/) is an open-source monitoring and alerting toolkit that focuses on reliability and scalability. Originally built by SoundCloud in 2012, Prometheus has since become a project under the Cloud Native Computing Foundation (CNCF). Key features include:

Key features include:
Multi-dimensional Data Model:
Prometheus uses a flexible data model based on key-value pairs called labels, which allows for highly granular and detailed data representation. This enables users to precisely query and aggregate metrics across various dimensions, such as instances, jobs, and environments.

PromQL (Prometheus Query Language):
Prometheus includes a powerful query language called PromQL, which allows users to perform complex queries on time-series data. With PromQL, users can aggregate, filter, and transform metrics in real-time, facilitating detailed analysis and visualization of system performance.

Time-Series Data Storage:
Prometheus stores all scraped metrics as time-series data, indexed by metric name and a set of key-value pairs. This approach allows for efficient storage and retrieval of large volumes of metrics data, making it ideal for monitoring large-scale environments.


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
* 

### **Running the Program**


* **Start Nvidia GPU Exporter, Node Exporter, Prometheus, AI carbon footprint tools Python server, responseAIProject**

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
  ```
  

* **AI carbon footprint tools Python server start process**
```
#Install Python 3.8 or Higher

#Install FastAPI and Unicorn

python -m pip install fastapi 
python -m pip install unicorn

#Start the Service
Open the command line terminal and navigate to the directory containing your main.py file. Start the service with the following command:
python -m uvicorn main:app --reload
```


* **ResponseAIProject** *

```
First, make sure you have install the JDK8 above, and the nodejs (version above 18), npm(version above 8) command in your machine.

1  git clone this folder to your machine
2  After finish, copy the CVS file to responseAIProject-/serve-end/, and change the names to "training_data.csv" or "inference_data.csv"
3  start the jar with: nohup  java -jar responseAIWeb-0.0.1-SNAPSHOT.jar >log.out &
4  Go to the responseAIProject-\responseAIWeb, exec the commands:
  1)  npm i serve -g
  2)  npm i
  3)  run command "npm run build"
     
 Afetr success build, there is "build" folder under responseAIWeb, go into "build" folder,
  5) nohup serve -s  -l 3033 & (Remember, this command must be you are in "build" folder)
  6) Then, access the page on any machine  , https://IP:3033
```


* **Modify the main code of the power_test target program**

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

* **Start the Target Program**

  ```sh
  python3 name_of_your_code.py
  ```

  Then, you can find the .csv file recording various information in the root directory of your target program

### Example

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

