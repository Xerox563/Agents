import time
import random
from typing import Callable, Any

def retry_with_backoff(
    func: Callable, 
    max_retries: int = 5, 
    initial_delay: float = 1.0, 
    backoff_factor: float = 2.0,
    jitter: bool = True
) -> Any:
    """
    Retry a function with exponential backoff and optional jitter.
    
    Why: LLM APIs (like OpenRouter) can occasionally fail due to rate limits or 
    transient network issues. Retrying ensures better reliability.
    """
    retries = 0
    delay = initial_delay

    while retries < max_retries:
        try:
            return func()
        except Exception as e:
            retries += 1
            if retries >= max_retries:
                print(f" All {max_retries} retries failed. Final error: {str(e)}")
                raise e
            
            # Calculate sleep time
            sleep_time = delay * (backoff_factor ** (retries - 1))
            if jitter:
                sleep_time += random.uniform(0, 0.1 * sleep_time)
            
            print(f" Attempt {retries} failed: {str(e)}. Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)

def openrouter_completion_with_retry(client, **kwargs):
    """
    Specific wrapper for OpenRouter chat completions with retry logic.
    """
    def call_completion():
        return client.chat.completions.create(**kwargs)
    
    return retry_with_backoff(call_completion)
