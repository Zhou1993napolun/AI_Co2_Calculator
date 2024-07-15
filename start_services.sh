#!/bin/bash

# Function to check if a process is running
check_process() {
    if pgrep -f "$1" > /dev/null
    then
        echo "$2 started successfully."
    else
        echo "Failed to start $2."
    fi
}

# Start Prometheus
echo "Starting Prometheus service..."
nohup ./prometheus --config.file=prometheus.yml > prometheus.log 2>&1 &
sleep 2  # Add some delay to allow the process to start
check_process "prometheus" "Prometheus service"

# Start GPU exporter
echo "Starting GPU exporter..."
nohup ./nvidia_gpu_exporter > nvidia_gpu_exporter.log 2>&1 &
sleep 2
check_process "nvidia_gpu_exporter" "GPU exporter"

# Start Node exporter
echo "Starting Node exporter..."
nohup ./node_exporter > node_exporter.log 2>&1 &
sleep 2
check_process "node_exporter" "Node exporter"

# 启动 Java 服务
echo "Starting Java service..."
cd ./dashboard/server-end/
nohup java -jar responseAIWeb-0.0.1-SNAPSHOT.jar > log.out &
sleep 2
check_process "responseAIWeb-0.0.1-SNAPSHOT.jar" "Java service"
cd -

# 启动 serve 静态服务器
echo "Starting serve static server (3033) ..."
cd ./dashboard/responseAIWeb/build/
nohup serve -s -l 3033 &
sleep 2
check_process "serve -s -l 3033" "serve static server"
cd -

# 启动 Python FastAPI 应用
echo "Starting Python FastAPI app..."
cd ./co2signal_api/
nohup python -m uvicorn main:app --reload &
sleep 2
check_process "uvicorn main:app" "Python FastAPI app"
cd -
