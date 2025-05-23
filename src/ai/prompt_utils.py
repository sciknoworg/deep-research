import os
import tiktoken
from typing import Optional
from ai.textsplitter import RecursiveCharacterTextSplitter

MIN_CHUNK_SIZE = 140

try:
    encoder = tiktoken.get_encoding('o200k_base')
except Exception:
    encoder = tiktoken.get_encoding('cl100k_base')

def trim_prompt(prompt: str, context_size: Optional[int] = None) -> str:
    """Trim prompt to fit within maximum context size."""
    if not prompt:
        return ''
    
    if context_size is None:
        context_size = int(os.getenv('CONTEXT_SIZE', '128000'))
    
    if not encoder:
        # Fallback: rough estimation (4 chars per token on average)
        if len(prompt) <= context_size * 4:
            return prompt
        return prompt[:context_size * 4]
    
    # Get token count
    tokens = encoder.encode(prompt)
    token_count = len(tokens)
    
    if token_count <= context_size:
        return prompt
    
    overflow_tokens = token_count - context_size
    
    # Estimate characters to remove (average 3 chars per token)
    chars_to_remove = overflow_tokens * 3
    chunk_size = len(prompt) - chars_to_remove
    
    if chunk_size < MIN_CHUNK_SIZE:
        return prompt[:MIN_CHUNK_SIZE]
    
    # Use text splitter to get first chunk
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=0
    )
    
    chunks = splitter.split_text(prompt)
    trimmed_prompt = chunks[0] if chunks else ''
    
    # Handle edge case where splitter doesn't reduce length
    if len(trimmed_prompt) == len(prompt):
        return trim_prompt(prompt[:chunk_size], context_size)
    
    # Recursively trim until within context size
    return trim_prompt(trimmed_prompt, context_size)
