import json
from pathlib import Path
from functools import lru_cache


depth_breadth_filename_patterns = ['d1_b1', 'd1_b4', 'd4_b1', 'd4_b4']
model_and_search_pattern = "o3-mini_orkg"
topic = "nlp" #"ecology"  # or "nlp"


@lru_cache
def load_domain_vocab(path: str = "vocab/nlp_dictionaries.json") -> dict:
    with Path(path).open() as fh:
        return json.load(fh)
