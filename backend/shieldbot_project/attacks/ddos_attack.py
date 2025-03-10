import subprocess
import logging
import os
import random

logger = logging.getLogger(__name__)

def ddos_attack_test(target_url, options=None):
    """
    Performs a DDoS attack simulation using GoldenEye.
    
    Args:
        target_url (str): The URL to target
        options (dict): Options including:
            - workers: Number of workers (default: 10)
            - sockets: Number of sockets (default: 30)
            - duration: Attack duration in seconds (default: 30)
    
    Returns:
        dict: Results of the attack test
    """
    if options is None:
        options = {}
    
    # Get parameters from options or use defaults
    workers = options.get('workers', 10)
    sockets = options.get('sockets', 30)
    duration = options.get('duration', 30)
    
    logs = []
    logs.append(f"Starting DDoS attack simulation on {target_url}")
    
    try:
        # Ensure GoldenEye script exists or is accessible
        goldeneye_path = options.get('goldeneye_path', './backend/attack_scripts/tools/goldeneye.py')
        
        if not os.path.exists(goldeneye_path):
            logs.append(f"Error: GoldenEye script not found at {goldeneye_path}")
            return {
                "logs": logs,
                "score": 0,
                "success": False,
                "error": "GoldenEye tool not found"
            }
        
        # Build command
        cmd = [
            'python', goldeneye_path, 
            target_url,
            '-w', str(workers),
            '-s', str(sockets),
            '-d', str(duration)
        ]
        
        logs.append(f"Executing command: {' '.join(cmd)}")
        
        # Execute the command with timeout
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for the process to complete or timeout
        stdout, stderr = process.communicate(timeout=duration + 10)
        
        # Log the results
        logs.append("DDoS attack complete")
        logs.append(f"Exit code: {process.returncode}")
        
        if stdout:
            logs.append("Output summary:")
            # Only include important parts of the output to avoid excessive logs
            for line in stdout.splitlines()[:20]:
                logs.append(line)
        
        if stderr:
            logs.append("Errors:")
            logs.append(stderr)
        
        return {
            "logs": logs,
            "score": 8 if process.returncode == 0 else 4,
            "success": process.returncode == 0,
            "details": {
                "workers": workers,
                "sockets": sockets,
                "duration": duration
            }
        }
        
    except subprocess.TimeoutExpired:
        logs.append("Attack timed out - this could mean it's still running")
        return {
            "logs": logs,
            "score": 5,
            "success": True,
            "timeout": True
        }
    except Exception as e:
        logs.append(f"Error performing DDoS attack: {str(e)}")
        return {
            "logs": logs,
            "score": 0,
            "success": False,
            "error": str(e)
        } 