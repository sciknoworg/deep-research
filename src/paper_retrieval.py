import os
import aiohttp
import json
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional

class ORKGAskClient:
    """
    Client for ORKG: uses the Ask index for search only (no per-paper fetch).
    Search endpoint: https://api.ask.orkg.org/index/search
    """
    def __init__(self, base_url: str = "https://api.ask.orkg.org/index"):
        self.base_url = base_url.rstrip("/")
        # Ensure data directory exists for logging raw responses
        self.data_dir = Path(__file__).parent.parent / "src/data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    async def search(self, query: str, limit: int = 10, timeout: int = 15) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/search"
        params = {"query": query, "limit": limit}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, timeout=timeout) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
            except Exception as e:
                print(f"[ORKG-ERR] Search failed for '{query}': {e}")
                return []
        # Log raw JSON to data folder
        uid = uuid.uuid4().hex
        #out_file = self.data_dir / f"orkg_search_{uid}.json"
        #out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        # Return list of items
        if isinstance(data.get('data'), list):
            return data['data']
        return data.get('payload', {}).get('items', [])
    
    async def fetch_document(self, document_id: str, timeout: int = 15) -> Dict[str, Any]:
        """
        Fetch full metadata for a given document from ORKG Ask API.
        """
        url = f"{self.base_url}/get/{document_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=timeout) as resp:
                    resp.raise_for_status()
                    doc = await resp.json()
            except Exception as e:
                print(f"[ORKG-ERR] fetch_document failed for '{document_id}': {e}")
                return {}
        # Log full doc JSON
        uid = uuid.uuid4().hex
        out_file = self.data_dir / f"orkg_doc_{uid}.json"
        out_file.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        return doc


class FirecrawlClient:
    """
    Client for Firecrawl API (markdown scrape of webpages).
    Endpoint: https://api.firecrawl.dev/v1/search
    """
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv('FIRECRAWL_KEY', '')
        self.base_url = (base_url or os.getenv('FIRECRAWL_BASE_URL', 'https://api.firecrawl.dev/v1')).rstrip("/")
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    async def search(self, query: str, limit: int = 10, timeout: int = 15) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/search"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {"query": query, "limit": limit, "timeout": timeout * 1000, "scrapeOptions": {"formats": ["markdown"]}}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=body, headers=headers, timeout=timeout) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
            except Exception as e:
                print(f"[FC-ERR] Search failed for '{query}': {e}")
                return []
        # Log raw JSON
        uid = uuid.uuid4().hex
        out_file = self.data_dir / f"firecrawl_search_{uid}.json"
        out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data.get('data', [])

# Factory to select client
from typing import Any

def get_search_client(provider: str) -> Any:
    provider = provider.lower()
    if provider == 'firecrawl':
        return FirecrawlClient()
    return ORKGAskClient()