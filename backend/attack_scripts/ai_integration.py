import requests
import json
import logging

logger = logging.getLogger(__name__)

def ai_decision(test_results, hf_key):
    """
    Use the Hugging Face Inference API to analyze test results and return recommendations.
    """
    prompt = "Analyze the following cyber security test results and provide recommendations for further intrusion methods: " + json.dumps(test_results)
    
    headers = {"Authorization": f"Bearer {hf_key}"}
    payload = {"inputs": prompt}
    
    try:
        response = requests.post("https://api-inference.huggingface.co/models/gpt2",
                                 headers=headers, json=payload, timeout=10)
        if response.ok:
            return response.json()
        else:
            logger.error("Hugging Face API error: %s", response.text)
            return {"recommendation": "Error in AI assessment", "confidence": 0.0}
    except Exception as e:
        logger.exception("Exception when calling Hugging Face API")
        return {"recommendation": "Error in AI assessment", "confidence": 0.0} 