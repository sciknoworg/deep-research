# thesis-scripts/factory.py
# Factory that returns the correct analyzer (Ecology or NLP) with robust imports.
# It also ensures the directories behave like packages in environments where
# relative imports could otherwise fail when running as a script.

from __future__ import annotations
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOMAINS_DIR = os.path.join(BASE_DIR, "domains")

# Ensure current dir is importable
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Make sure we have package markers to stabilize imports on some setups
for p in (BASE_DIR, DOMAINS_DIR):
    try:
        init_path = os.path.join(p, "__init__.py")
        if not os.path.exists(init_path):
            open(init_path, "a").close()
    except Exception:
        pass

# Import analyzers (absolute first, fallback to relative)
try:
    from domains.ecology import EcologyAnalyzer  # type: ignore
    from domains.nlp import NLPAnalyzer          # type: ignore
except Exception:
    from .domains.ecology import EcologyAnalyzer  # type: ignore
    from .domains.nlp import NLPAnalyzer          # type: ignore

try:
    from utils import topic  # expected to be "ecology" | "nlp"
except Exception:
    from .utils import topic  # type: ignore


def get_analyzer(custom_config=None, topic_override: str | None = None):
    """
    Return an analyzer instance for the requested topic.
    - custom_config: optional ScoringConfig
    - topic_override: set to "ecology" or "nlp" to override utils.topic
    """
    t = (topic_override or str(topic) or "ecology").strip().lower()
    if t == "nlp":
        return NLPAnalyzer(config=custom_config)
    return EcologyAnalyzer(config=custom_config)
