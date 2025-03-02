import socket
import logging
import concurrent.futures
import time
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def port_scan_test(target_url, options=None):
    """
    Performs a port scan on a target URL.
    
    Args:
        target_url (str): The URL to scan
        options (dict): Options including:
            - port_range: Range of ports to scan (default: [20-25, 80, 443, 8080, 8443])
            - timeout: Connection timeout in seconds (default: 1)
            - max_workers: Maximum concurrent workers (default: 10)
    
    Returns:
        dict: Results of the port scan
    """
    if options is None:
        options = {}
    
    logs = []
    logs.append(f"Starting port scan on {target_url}")
    
    try:
        # Parse URL to get hostname
        parsed_url = urlparse(target_url)
        hostname = parsed_url.netloc.split(':')[0]
        
        if not hostname:
            logs.append("Error: Could not extract hostname from URL")
            return {
                "logs": logs,
                "score": 0,
                "success": False,
                "error": "Invalid URL format"
            }
        
        logs.append(f"Resolved hostname: {hostname}")
        
        # Get configuration
        port_range = options.get('port_range', [20, 21, 22, 23, 25, 80, 443, 8080, 8443])
        timeout = options.get('timeout', 1)
        max_workers = options.get('max_workers', 10)
        
        # Expand port range if specified as start-end
        expanded_port_range = []
        for port in port_range:
            if isinstance(port, str) and '-' in port:
                start, end = map(int, port.split('-'))
                expanded_port_range.extend(range(start, end + 1))
            else:
                expanded_port_range.append(int(port))
        
        logs.append(f"Scanning {len(expanded_port_range)} ports with timeout {timeout}s")
        
        # Function to check a single port
        def check_port(port):
            start_time = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            result = s.connect_ex((hostname, port))
            s.close()
            elapsed = time.time() - start_time
            return port, result == 0, elapsed
        
        # Scan ports in parallel
        open_ports = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_port = {executor.submit(check_port, port): port for port in expanded_port_range}
            for future in concurrent.futures.as_completed(future_to_port):
                port, is_open, elapsed = future.result()
                if is_open:
                    logs.append(f"Port {port} is open (response time: {elapsed:.4f}s)")
                    open_ports.append(port)
        
        logs.append(f"Scan complete. Found {len(open_ports)} open ports.")
        
        # Try to identify common services on open ports
        common_services = {
            20: "FTP Data",
            21: "FTP Control",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            80: "HTTP",
            443: "HTTPS",
            3306: "MySQL",
            5432: "PostgreSQL",
            8080: "HTTP Alternate",
            8443: "HTTPS Alternate",
            27017: "MongoDB",
            6379: "Redis"
        }
        
        service_details = []
        for port in open_ports:
            service = common_services.get(port, "Unknown")
            service_details.append({"port": port, "service": service})
            
        return {
            "logs": logs,
            "score": 7 if open_ports else 3,
            "success": True,
            "details": {
                "open_ports": open_ports,
                "services": service_details,
                "total_scanned": len(expanded_port_range)
            }
        }
        
    except Exception as e:
        logs.append(f"Error during port scan: {str(e)}")
        return {
            "logs": logs,
            "score": 0,
            "success": False,
            "error": str(e)
        } 