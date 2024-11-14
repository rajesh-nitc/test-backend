from typing import Any
from tools.spend import spend_tool
from util import extract_function_calls, extract_text
import logging
from vertexai.generative_models import (
    GenerativeModel, 
)

logger = logging.getLogger(__name__)

def process_prompt(prompt: str, model: GenerativeModel) -> str:
    response = model.generate_content(
    prompt,
    tools=[spend_tool],
    )
    
    function_calls = extract_function_calls(response)
    
    if len(function_calls) > 0:
        # Iterate through the list
        for item in function_calls:
            # item is a dictionary, so iterate through its key-value pairs
            for k, v in item.items():
                if k == 'get_spend_func':
                    logger.info(f"This is v: {v}")
        return v
    
    return extract_text(response)
