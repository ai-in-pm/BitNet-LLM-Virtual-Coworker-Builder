"""
Web-based monitoring dashboard for BitNet Virtual Co-worker Builder.
"""

import os
import json
import time
import datetime
import argparse
import logging
from pathlib import Path
import threading
import subprocess
import platform

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psutil
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Default paths
DEFAULT_INSTALL_DIR = r"C:\BitNet-VC-Builder"
DEFAULT_MONITORING_DIR = os.path.join(DEFAULT_INSTALL_DIR, "monitoring")
DEFAULT_SUMMARY_FILE = os.path.join(DEFAULT_MONITORING_DIR, "summary.json")
DEFAULT_LOG_DIR = os.path.join(DEFAULT_INSTALL_DIR, "logs")

# Global variables
monitoring_data = []
system_metrics = []

def run_monitoring_script(install_dir):
    """Run the monitoring script to collect data."""
    monitor_script = os.path.join(install_dir, "monitoring", "monitor.ps1")
    
    if not os.path.exists(monitor_script):
        logger.error(f"Monitoring script not found: {monitor_script}")
        return False
    
    try:
        if platform.system() == "Windows":
            subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", monitor_script, "-Silent"],
                check=True
            )
        else:
            logger.error("This script is designed to run on Windows")
            return False
        
        logger.info("Monitoring script executed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run monitoring script: {e}")
        return False

def load_monitoring_data(summary_file):
    """Load monitoring data from the summary file."""
    if not os.path.exists(summary_file):
        return None
    
    try:
        with open(summary_file, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f"Failed to load monitoring data: {e}")
        return None

def collect_system_metrics():
    """Collect current system metrics."""
    metrics = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }
    return metrics

def check_service_status(url):
    """Check if a service is responding."""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def background_monitoring(install_dir, summary_file, interval=60):
    """Background thread for continuous monitoring."""
    global monitoring_data, system_metrics
    
    while True:
        # Run the monitoring script
        run_monitoring_script(install_dir)
        
        # Load the monitoring data
        data = load_monitoring_data(summary_file)
        if data:
            monitoring_data.append(data)
            # Keep only the last 100 data points
            if len(monitoring_data) > 100:
                monitoring_data = monitoring_data[-100:]
        
        # Collect system metrics
        metrics = collect_system_metrics()
        system_metrics.append(metrics)
        # Keep only the last 100 data points
        if len(system_metrics) > 100:
            system_metrics = system_metrics[-100:]
        
        # Sleep for the specified interval
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description="Web-based monitoring dashboard for BitNet Virtual Co-worker Builder")
    parser.add_argument("--install-dir", default=DEFAULT_INSTALL_DIR, help="Installation directory")
    parser.add_argument("--port", type=int, default=8502, help="Port to run the dashboard on")
    args = parser.parse_args()
    
    install_dir = args.install_dir
    monitoring_dir = os.path.join(install_dir, "monitoring")
    summary_file = os.path.join(monitoring_dir, "summary.json")
    log_dir = os.path.join(install_dir, "logs")
    
    # Create monitoring directory if it doesn't exist
    os.makedirs(monitoring_dir, exist_ok=True)
    
    # Start background monitoring thread
    monitoring_thread = threading.Thread(
        target=background_monitoring,
        args=(install_dir, summary_file, 60),
        daemon=True
    )
    monitoring_thread.start()
    
    # Run Streamlit app
    st.title("BitNet Virtual Co-worker Builder Monitoring Dashboard")
    
    # Refresh button
    if st.button("Refresh Data"):
        run_monitoring_script(install_dir)
    
    # Display current status
    st.header("Current Status")
    
    # Load the latest monitoring data
    data = load_monitoring_data(summary_file)
    
    if data:
        # Create columns for service status
        col1, col2 = st.columns(2)
        
        # API Server status
        with col1:
            api_status = "Running" if data.get("ApiServerRunning", False) and data.get("ApiServerResponding", False) else "Not Running"
            api_color = "green" if api_status == "Running" else "red"
            st.markdown(f"**API Server:** <span style='color:{api_color}'>{api_status}</span>", unsafe_allow_html=True)
        
        # Web UI status
        with col2:
            web_status = "Running" if data.get("WebUiRunning", False) and data.get("WebUiResponding", False) else "Not Running"
            web_color = "green" if web_status == "Running" else "red"
            st.markdown(f"**Web UI:** <span style='color:{web_color}'>{web_status}</span>", unsafe_allow_html=True)
        
        # Create columns for system resources
        col1, col2, col3 = st.columns(3)
        
        # Disk space
        with col1:
            disk_free = data.get("DiskSpaceFreeGB", 0)
            disk_percent = data.get("DiskSpaceFreePercentage", 0)
            disk_color = "green"
            if disk_percent < 20:
                disk_color = "orange"
            if disk_percent < 10:
                disk_color = "red"
            st.markdown(f"**Disk Space:** <span style='color:{disk_color}'>{disk_free:.2f} GB free ({disk_percent:.2f}%)</span>", unsafe_allow_html=True)
        
        # CPU usage
        with col2:
            cpu_percent = data.get("CpuUsagePercentage", 0)
            cpu_color = "green"
            if cpu_percent > 80:
                cpu_color = "orange"
            if cpu_percent > 90:
                cpu_color = "red"
            st.markdown(f"**CPU Usage:** <span style='color:{cpu_color}'>{cpu_percent:.2f}%</span>", unsafe_allow_html=True)
        
        # Memory usage
        with col3:
            memory_percent = data.get("MemoryUsagePercentage", 0)
            memory_color = "green"
            if memory_percent > 80:
                memory_color = "orange"
            if memory_percent > 90:
                memory_color = "red"
            st.markdown(f"**Memory Usage:** <span style='color:{memory_color}'>{memory_percent:.2f}%</span>", unsafe_allow_html=True)
        
        # Error count
        error_count = data.get("ErrorCount", 0)
        error_color = "green"
        if error_count > 0:
            error_color = "orange"
        if error_count > 20:
            error_color = "red"
        st.markdown(f"**Recent Errors:** <span style='color:{error_color}'>{error_count}</span>", unsafe_allow_html=True)
        
        # Last update time
        st.markdown(f"**Last Update:** {data.get('Timestamp', 'Unknown')}")
    else:
        st.error("No monitoring data available. Please run the monitoring script first.")
    
    # Display historical data
    st.header("Historical Data")
    
    if monitoring_data:
        # Convert monitoring data to DataFrame
        df = pd.DataFrame(monitoring_data)
        
        # Convert timestamp to datetime
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        
        # Create tabs for different metrics
        tab1, tab2, tab3, tab4 = st.tabs(["CPU Usage", "Memory Usage", "Disk Space", "Service Status"])
        
        # CPU Usage tab
        with tab1:
            fig = px.line(df, x="Timestamp", y="CpuUsagePercentage", title="CPU Usage Over Time")
            fig.update_layout(yaxis_title="CPU Usage (%)")
            st.plotly_chart(fig)
        
        # Memory Usage tab
        with tab2:
            fig = px.line(df, x="Timestamp", y="MemoryUsagePercentage", title="Memory Usage Over Time")
            fig.update_layout(yaxis_title="Memory Usage (%)")
            st.plotly_chart(fig)
        
        # Disk Space tab
        with tab3:
            fig = px.line(df, x="Timestamp", y="DiskSpaceFreePercentage", title="Free Disk Space Over Time")
            fig.update_layout(yaxis_title="Free Disk Space (%)")
            st.plotly_chart(fig)
        
        # Service Status tab
        with tab4:
            # Create a DataFrame for service status
            service_data = []
            for data in monitoring_data:
                timestamp = data.get("Timestamp")
                api_status = 1 if data.get("ApiServerRunning", False) and data.get("ApiServerResponding", False) else 0
                web_status = 1 if data.get("WebUiRunning", False) and data.get("WebUiResponding", False) else 0
                service_data.append({"Timestamp": timestamp, "API Server": api_status, "Web UI": web_status})
            
            service_df = pd.DataFrame(service_data)
            service_df["Timestamp"] = pd.to_datetime(service_df["Timestamp"])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=service_df["Timestamp"], y=service_df["API Server"], mode="lines", name="API Server"))
            fig.add_trace(go.Scatter(x=service_df["Timestamp"], y=service_df["Web UI"], mode="lines", name="Web UI"))
            fig.update_layout(title="Service Status Over Time", yaxis_title="Status (1=Up, 0=Down)")
            st.plotly_chart(fig)
    else:
        st.info("No historical data available yet. Data will be collected automatically.")
    
    # Display recent logs
    st.header("Recent Logs")
    
    # Get log files
    log_files = []
    if os.path.exists(log_dir):
        log_files = [f for f in os.listdir(log_dir) if f.endswith(".log")]
    
    if log_files:
        selected_log = st.selectbox("Select Log File", log_files)
        log_path = os.path.join(log_dir, selected_log)
        
        try:
            with open(log_path, "r") as f:
                # Get the last 100 lines
                lines = f.readlines()[-100:]
                log_content = "".join(lines)
            
            st.text_area("Log Content", log_content, height=300)
        except Exception as e:
            st.error(f"Failed to read log file: {e}")
    else:
        st.info("No log files found.")
    
    # Actions section
    st.header("Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Restart API Server"):
            try:
                # Kill existing process
                subprocess.run(["taskkill", "/f", "/im", "python.exe", "/fi", "WINDOWTITLE eq BitNet VC Builder - API Server"], check=False)
                # Start new process
                subprocess.Popen(["powershell", "-Command", f"Start-Process -FilePath '{install_dir}\\venv\\Scripts\\python.exe' -ArgumentList '-m bitnet_vc_builder.api.server --config {install_dir}\\config\\config.yaml' -WindowStyle Normal -WorkingDirectory '{install_dir}'"])
                st.success("API Server restarted")
            except Exception as e:
                st.error(f"Failed to restart API Server: {e}")
    
    with col2:
        if st.button("Restart Web UI"):
            try:
                # Kill existing process
                subprocess.run(["taskkill", "/f", "/im", "python.exe", "/fi", "WINDOWTITLE eq BitNet VC Builder - Web UI"], check=False)
                # Start new process
                subprocess.Popen(["powershell", "-Command", f"Start-Process -FilePath '{install_dir}\\venv\\Scripts\\python.exe' -ArgumentList '-m bitnet_vc_builder.ui.web.app --config {install_dir}\\config\\config.yaml' -WindowStyle Normal -WorkingDirectory '{install_dir}'"])
                st.success("Web UI restarted")
            except Exception as e:
                st.error(f"Failed to restart Web UI: {e}")
    
    # Add auto-refresh
    st.markdown("""
    <script>
        var timeout = setTimeout(function() {
            window.location.reload();
        }, 60000);
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
