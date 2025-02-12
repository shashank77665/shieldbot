import requests
import json
import logging
from transformers import GPT2Tokenizer

logger = logging.getLogger(__name__)

# Load the tokenizer once for token-trimming purposes.
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def trim_prompt(prompt, max_tokens=1022, reserved_tokens=0):
    """
    Trims the prompt so that (prompt tokens + reserved tokens) does not exceed max_tokens.
    Uses the GPT-2 tokenizer for accurate token counting.
    
    Args:
        prompt (str): The input prompt.
        max_tokens (int): Maximum total tokens allowed.
        reserved_tokens (int): Tokens reserved for model generation (if any).
    
    Returns:
        str: Trimmed prompt.
    """
    tokens = tokenizer.encode(prompt, add_special_tokens=False)
    allowed_tokens = max_tokens - reserved_tokens
    if len(tokens) > allowed_tokens:
        tokens = tokens[:allowed_tokens]
        prompt = tokenizer.decode(tokens)
    return prompt

def ai_decision(test_results, hf_key):
    """
    Use the Hugging Face Inference API to analyze test results and return recommendations.
    
    Args:
        test_results (dict): Dictionary containing test results/logs.
        hf_key (str): Hugging Face API key.
        
    Returns:
        dict: Contains recommendation and a confidence score.
    """
    # Verify that the API key is provided.
    if not hf_key:
        logger.error("No Hugging Face API key provided. Please set HF_API_KEY in your environment or configuration.")
        return {"recommendation": "Invalid API key", "confidence": 0.0}
    
    # Build the prompt from test_results.
    prompt = (
        "Analyze the following cyber security test results and provide recommendations "
        "for further intrusion methods: " + json.dumps(test_results)
    )
    
    # Trim the prompt to be within the token limits.
    trimmed_prompt = trim_prompt(prompt, max_tokens=1022, reserved_tokens=0)
    
    # Print the (possibly trimmed) test results/prompt to terminal before sending.
    print("Test results (prompt) being sent to GPT-2:")
    print(trimmed_prompt)
    
    headers = {"Authorization": f"Bearer {hf_key}"}
    payload = {"inputs": trimmed_prompt}
    
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers=headers,
            json=payload,
            timeout=10
        )
        if response.ok:
            return response.json()
        else:
            if response.status_code == 401:
                logger.error("Hugging Face API unauthorized. Verify that HF_API_KEY is valid. Response: %s", response.text)
            else:
                logger.error("Hugging Face API error: %s", response.text)
            return {"recommendation": "Error in AI assessment", "confidence": 0.0}
    except Exception as e:
        logger.exception("Exception when calling Hugging Face API")
        return {"recommendation": "Error in AI assessment", "confidence": 0.0} 