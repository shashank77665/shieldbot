def create_result(logs=None, score=0, success=True, error=None):
    """
    Helper function that creates a standardized result dictionary for attack tests.
    
    Args:
        logs (list): List of log messages from the test.
        score (int or float): Severity score or success metric.
        success (bool): True if the test indicates a vulnerability or positive test outcome.
        error (str, optional): Any error message encountered during the test.

    Returns:
        dict: A dictionary containing the test outcome.
    """
    return {
        "logs": logs if logs is not None else [],
        "score": score,
        "success": success,
        "error": error
    }