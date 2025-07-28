# monitoring/metrics.py
from prometheus_client import Counter, Histogram, start_http_server
import time
import psutil
import logging

class MetricsCollector:
    def __init__(self):
        self.api_requests = Counter('api_requests_total', 'Total API requests')
        self.generation_time = Histogram('generation_seconds', 'Time spent generating code')
        self.cpu_usage = Histogram('cpu_usage_percent', 'CPU usage percentage')
        self.memory_usage = Histogram('memory_usage_bytes', 'Memory usage in bytes')
        
        # Start Prometheus metrics server
        start_http_server(8000)
    
    def track_request(self):
        self.api_requests.inc()
    
    def track_generation(self, start_time):
        self.generation_time.observe(time.time() - start_time)
    
    def collect_system_metrics(self):
        self.cpu_usage.observe(psutil.cpu_percent())
        self.memory_usage.observe(psutil.Process().memory_info().rss)

# monitoring/logger.py
class Logger:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_generation(self, prompt: str, result: str):
        self.logger.info(f"Generated code for prompt: {prompt[:100]}...")
        
    def log_error(self, error: Exception):
        self.logger.error(f"Error occurred: {str(error)}")
