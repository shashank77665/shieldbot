import socket
import requests
import logging

logger = logging.getLogger(__name__)

def ip_location_test(target_url, options=None):
    """
    Performs an IP geolocation lookup for a target URL.
    
    Args:
        target_url (str): The URL to lookup
        options (dict): Options for the lookup
    
    Returns:
        dict: Results of the IP location lookup
    """
    if options is None:
        options = {}
    
    logs = []
    logs.append(f"Starting IP location lookup for {target_url}")
    
    try:
        # Extract domain from URL
        if "://" in target_url:
            domain = target_url.split("://")[1].split("/")[0]
        else:
            domain = target_url.split("/")[0]
            
        # Remove port if present
        if ":" in domain:
            domain = domain.split(":")[0]
            
        logs.append(f"Resolved domain: {domain}")
        
        # Get IP address
        ip_address = socket.gethostbyname(domain)
        logs.append(f"IP address: {ip_address}")
        
        # Use public API for geolocation
        # Note: In production, consider using a paid service with API key
        response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant information
            location_info = {
                "ip": ip_address,
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country_name", "Unknown"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "org": data.get("org", "Unknown"),
                "timezone": data.get("timezone", "Unknown")
            }
            
            logs.append(f"Location: {location_info['city']}, {location_info['region']}, {location_info['country']}")
            logs.append(f"Coordinates: {location_info['latitude']}, {location_info['longitude']}")
            logs.append(f"Organization: {location_info['org']}")
            
            return {
                "logs": logs,
                "score": 8,
                "success": True,
                "details": location_info
            }
        else:
            logs.append(f"Error from geolocation API: {response.status_code}")
            return {
                "logs": logs,
                "score": 3,
                "success": False,
                "error": f"API returned status code {response.status_code}"
            }
            
    except socket.gaierror:
        logs.append(f"Could not resolve host: {domain}")
        return {
            "logs": logs,
            "score": 0,
            "success": False,
            "error": "Domain could not be resolved to an IP address"
        }
    except Exception as e:
        logs.append(f"Error during IP location lookup: {str(e)}")
        return {
            "logs": logs,
            "score": 0,
            "success": False,
            "error": str(e)
        } 